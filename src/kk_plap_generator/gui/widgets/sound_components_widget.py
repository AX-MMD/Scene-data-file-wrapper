import math
import tkinter as tk
import typing
from tkinter import simpledialog

from kk_plap_generator.gui import info_text
from kk_plap_generator.gui.info_message import InfoMessageFrame
from kk_plap_generator.gui.widgets.base import PlapWidget
from kk_plap_generator.models import SoundComponentConfig

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class SoundComponentsWidget(PlapWidget):
    def __init__(self, app: "PlapUI", masterframe):
        super().__init__(app, masterframe)

        self.sound_components_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.sound_components_frame.grid(row=0, column=0, sticky="nsew")

        # Top
        self.top_frame = tk.Frame(self.sound_components_frame)
        self.top_frame.grid_columnconfigure(0, weight=90)
        self.top_frame.grid_columnconfigure(1, weight=10)
        self.top_frame.pack(fill=tk.X)

        # Sound Components
        self.top_left_frame = tk.Frame(self.top_frame)
        self.top_left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.sound_components_label = tk.Label(
            self.top_left_frame, text="Sound Components"
        )
        self.sound_components_label.pack()

        info_message = info_text.SOUND_FOLDERS
        self.top_right_frame = InfoMessageFrame(self.top_frame, info_message)

        self.sound_components_listbox = tk.Listbox(self.sound_components_frame)
        self.sound_components_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sound_components_listbox.bind("<Double-Button-1>", self.edit_sound_component)

        self.sound_components_scrollbar = tk.Scrollbar(
            self.sound_components_frame, orient="vertical"
        )
        self.sound_components_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sound_components_listbox.config(
            yscrollcommand=self.sound_components_scrollbar.set
        )
        self.sound_components_scrollbar.config(
            command=self.sound_components_listbox.yview
        )

        self.update()

        self.add_sound_component_name_button = tk.Button(
            self.sound_components_frame, text="+", command=self.add_sound_component
        )
        self.add_sound_component_name_button.pack(fill=tk.X)

        self.remove_sound_component_name_button = tk.Button(
            self.sound_components_frame,
            text="-",
            command=self.remove_selected_sound_component,
        )
        self.remove_sound_component_name_button.pack(fill=tk.X)

    def update(self):
        self.sound_components_listbox.delete(0, tk.END)
        for sc in self.app.store["sound_components"]:
            offset_str = f"  ({'+' if sc['offset'] >= 0 else '-'}{abs(sc['offset'])}s)"
            cutoff_str = f"(end:{sc['cutoff']}s)" if sc["cutoff"] != math.inf else ""
            self.sound_components_listbox.insert(
                tk.END, f"{sc['name']}{offset_str}{cutoff_str}"
            )

    def edit_sound_component(self, event):
        selected_index = self.sound_components_listbox.curselection()
        if not selected_index:
            return

        index: int = selected_index[0]
        component = self.app.store["sound_components"][index]

        dialog = SoundComponentDialog(
            self.masterframe,
            title="Edit Sound Component",
            name=component["name"],
            offset=component["offset"],
            cutoff=component["cutoff"],
        )

        if dialog.is_valid():
            component["name"] = dialog.name
            component["offset"] = dialog.offset
            component["cutoff"] = dialog.cutoff
            self.update()

    def add_sound_component(self):
        dialog = SoundComponentDialog(self.masterframe, title="Add Sound Component")
        sound_component = SoundComponentConfig(
            name=dialog.name, offset=dialog.offset, cutoff=dialog.cutoff
        )
        self.app.store["sound_components"].append(sound_component)
        self.update()

    def remove_selected_sound_component(self):
        selected_index = self.sound_components_listbox.curselection()
        if selected_index:
            self.app.store["sound_components"].pop(selected_index[0])
            self.update()


class SoundComponentDialog(simpledialog.Dialog):
    def __init__(
        self,
        parent,
        title=None,
        name: str = "",
        offset: float = 0.0,
        cutoff: float = math.inf,
    ):
        self.name = name
        self.offset = offset or 0.0  # get rid of -0.0
        self.cutoff = cutoff
        self.ok_text = "✔"
        self.cancel_text = "✖"
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Name:").grid(row=0)
        tk.Label(master, text="Offset (sec):").grid(row=1)
        tk.Label(master, text="Cutoff (sec):").grid(row=2)

        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1)

        self.offset_entry = tk.Entry(master)
        self.offset_entry.grid(row=1, column=1)

        self.cutoff_entry = tk.Entry(master)
        self.cutoff_entry.grid(row=2, column=1)

        self.name_entry.insert(0, self.name)
        self.offset_entry.insert(0, str(self.offset))
        self.cutoff_entry.insert(0, str(self.cutoff if self.cutoff != math.inf else ""))

        return self.name_entry  # initial focus

    def buttonbox(self):
        box = tk.Frame(self)

        self.ok_button = tk.Button(
            box,
            text=self.ok_text,
            width=10,
            fg="green",
            command=self.ok,
            default=tk.ACTIVE,
        )
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button = tk.Button(
            box, text=self.cancel_text, width=10, fg="red", command=self.cancel
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def is_valid(self):
        return self.name != ""

    def apply(self):
        self.name = self.name_entry.get()

        try:
            self.offset = float(self.offset_entry.get())
        except ValueError:
            self.offset = 0.0

        try:
            self.cutoff = float(self.cutoff_entry.get())
        except ValueError:
            self.cutoff = math.inf
