import os
import tkinter as tk
import typing
from tkinter import filedialog

import tkinterdnd2

from kk_plap_generator.gui.widgets.base import PlapWidget

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class DnDWidget(PlapWidget):
    def __init__(self, app: "PlapUI", masterframe):
        super().__init__(app, masterframe)
        self.single_file: typing.Optional[str] = None

        self.drag_drop_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.drag_drop_frame.grid(row=0, column=0, sticky="nsew")
        self.drag_drop_label = tk.Label(
            self.drag_drop_frame, text="Drop the Single File here"
        )
        self.drag_drop_label.pack(fill=tk.BOTH, expand=True)
        self.drag_drop_label.drop_target_register(tkinterdnd2.DND_FILES)  # type: ignore

        self.drag_drop_label.dnd_bind("<<Drop>>", self.on_drop)  # type: ignore

        self.select_file_button = tk.Button(
            self.drag_drop_frame, text="Select File", command=self.select_file
        )
        self.select_file_button.pack()

    def get_single_file(self):
        return self.single_file

    def reset_single_file(self):
        self.single_file = None
        self.drag_drop_label.config(text="Drop the Single File here")

    def on_drop(self, event):
        self.single_file = event.data[1:-1]
        self.drag_drop_label.config(
            text=f"[ {os.path.basename(typing.cast(str, self.single_file))} ]"
        )

    def select_file(self):
        file_path = filedialog.askopenfilename(parent=self.app.master)
        if file_path:
            self.single_file = file_path
