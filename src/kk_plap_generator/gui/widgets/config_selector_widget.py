import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from kk_plap_generator import settings
from kk_plap_generator.gui.widgets.base import PlapWidget


class ConfigSelectorWidget(PlapWidget):
    def __init__(self, app, masterframe):
        super().__init__(app, masterframe)
        self.create_widgets()

    def create_widgets(self):
        self.select_config_button = tk.Button(
            self.masterframe, text="Load", command=self.open_config_dialog
        )
        self.select_config_button.grid(row=0, column=0, sticky="nsew")

    def open_config_dialog(self):
        file_path = filedialog.askopenfilename(
            initialdir=settings.CONFIG_FOLDER,
            title="Select Config File",
            filetypes=(("TOML files", "*.toml"), ("All files", "*.*"))
        )
        if file_path:
            self.load_selected_config(file_path)

    def load_selected_config(self, file_path):
        try:
            self.app.load_config(file_path)
            self.app.update_widgets()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config file: {e}")
