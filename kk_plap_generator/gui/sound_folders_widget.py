import tkinter as tk
import typing
from tkinter import simpledialog

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class SoundFoldersWidget:
    def __init__(self, app: "PlapUI", masterframe):
        self.app = app
        self.masterframe = masterframe
        self.store = app.store

        self.sound_folders_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.sound_folders_frame.grid(row=0, column=0, sticky="nsew")
        self.sound_folders_label = tk.Label(
            self.sound_folders_frame, text="Sound Folders"
        )
        self.sound_folders_label.pack()

        self.sound_folders_listbox = tk.Listbox(self.sound_folders_frame)
        self.sound_folders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sound_folders_scrollbar = tk.Scrollbar(
            self.sound_folders_frame, orient="vertical"
        )
        self.sound_folders_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sound_folders_listbox.config(yscrollcommand=self.sound_folders_scrollbar.set)
        self.sound_folders_scrollbar.config(command=self.sound_folders_listbox.yview)

        self.update()

        self.add_sound_folder_name_button = tk.Button(
            self.sound_folders_frame, text="+", command=self.add_sound_folder_name
        )
        self.add_sound_folder_name_button.pack(fill=tk.X)

        self.remove_sound_folder_name_button = tk.Button(
            self.sound_folders_frame,
            text="-",
            command=self.remove_selected_sound_folder_name,
        )
        self.remove_sound_folder_name_button.pack(fill=tk.X)

    def update(self):
        self.sound_folders_listbox.delete(0, tk.END)
        for name in self.store["plap_folder_names"]:
            self.sound_folders_listbox.insert(tk.END, name)

    def add_sound_folder_name(self):
        dialog = CustomDialog(self.masterframe, title="Add Sound Folder")
        name = dialog.result
        if name:
            self.store["plap_folder_names"].append(name)
            self.update()

    def remove_selected_sound_folder_name(self):
        selected_index = self.sound_folders_listbox.curselection()
        if selected_index:
            selected_name = self.sound_folders_listbox.get(selected_index)
            self.store["plap_folder_names"].remove(selected_name)
            self.update()


class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.ok_text = "✔"
        self.cancel_text = "✖"
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Enter folder name:").grid(row=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=0, column=1)
        return self.entry  # initial focus

    def buttonbox(self):
        box = tk.Frame(self)

        self.ok_button = tk.Button(box, text=self.ok_text, width=10, fg="green", command=self.ok, default=tk.ACTIVE)
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button = tk.Button(box, text=self.cancel_text, width=10, fg="red", command=self.cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        self.result = self.entry.get()
