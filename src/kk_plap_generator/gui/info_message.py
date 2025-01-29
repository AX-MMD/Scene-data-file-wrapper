import tkinter as tk
from tkinter import simpledialog

from kk_plap_generator.gui.output_mesage_box import CustomMessageBox


class InfoMessageFrame:
    def __init__(self, masterframe, message, text="ℹ", fg="blue"):
        self.message = message
        self.top_right_frame = tk.Frame(masterframe)
        self.top_right_frame.pack(side=tk.RIGHT)
        self.info_button = tk.Button(
            self.top_right_frame, text=text, fg=fg, command=self.show_info
        )
        self.info_button.pack(side=tk.RIGHT)

    def show_info(self):
        CustomMessageBox(self.top_right_frame, "Information", self.message)


class CustomInfoDialog(simpledialog.Dialog):
    def __init__(self, parent, message, title=None):
        self.message = message
        self.cancel_text = "✖"
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.message, justify="left").pack(padx=20, pady=20)
        return master

    def buttonbox(self):
        box = tk.Frame(self)

        self.cancel_button = tk.Button(
            box, text=self.cancel_text, width=10, command=self.cancel
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.bind("<Escape>", self.cancel)

        box.pack()
