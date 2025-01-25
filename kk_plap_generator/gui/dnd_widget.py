import tkinter as tk
from tkinter import filedialog
import tkinterdnd2
import typing

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI

class DnDWidget:
    def __init__(self, app: "PlapUI", masterframe):
        self.app = app
        self.masterframe = masterframe

        app.drag_drop_frame = tk.Frame(masterframe, bd=2, relief="solid")
        app.drag_drop_frame.grid(row=0, column=0, sticky="nsew")
        app.drag_drop_label = tk.Label(
            app.drag_drop_frame, text="Drop the Single File here"
        )
        app.drag_drop_label.pack(fill=tk.BOTH, expand=True)
        app.drag_drop_label.drop_target_register(tkinterdnd2.DND_FILES)

        app.drag_drop_label.dnd_bind("<<Drop>>", self.on_drop)

        app.select_file_button = tk.Button(
            app.drag_drop_frame, text="Select File", command=self.select_file
        )
        app.select_file_button.pack()

    def on_drop(self, event):
        self.app.ref_single_file = event.data

    def select_file(self):
        file_path = filedialog.askopenfilename(parent=self.app.master)
        if file_path:
            self.app.single_file = file_path
