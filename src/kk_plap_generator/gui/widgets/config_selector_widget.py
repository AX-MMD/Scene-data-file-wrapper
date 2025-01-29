import os
import tkinter as tk
from tkinter import messagebox

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
        self.dialog = tk.Toplevel(self.masterframe)
        self.dialog.title("Select Config File")
        self.dialog.geometry("300x200")

        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(0, weight=1)

        self.config_listbox = tk.Listbox(self.dialog, selectmode=tk.SINGLE)
        self.config_listbox.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.dialog, orient="vertical")
        self.scrollbar.config(command=self.config_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.config_listbox.config(yscrollcommand=self.scrollbar.set)

        config_files = [
            f
            for f in os.listdir(settings.CONFIG_FOLDER)
            if f.endswith(".toml") and f != os.path.basename(settings.CONFIG_FILE)
        ]
        for file in config_files:
            self.config_listbox.insert(tk.END, file)

        self.button_frame = tk.Frame(self.dialog)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=5)

        self.load_button = tk.Button(
            self.button_frame, text="✔", command=self.load_selected_config
        )
        self.load_button.grid(row=0, column=0, padx=5)

        self.cancel_button = tk.Button(
            self.button_frame, text="✖", command=self.dialog.destroy
        )
        self.cancel_button.grid(row=0, column=1, padx=5)

        self.dialog.lift()  # Bring the dialog to the front
        self.dialog.grab_set()  # Make the dialog modal
        self.dialog.update_idletasks()
        self.center_dialog()

    def center_dialog(self):
        self.dialog.update_idletasks()
        app_x = self.app.winfo_rootx()
        app_y = self.app.winfo_rooty()
        app_width = self.app.winfo_width()
        app_height = self.app.winfo_height()

        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()

        x = app_x + (app_width // 2) - (dialog_width // 2)
        y = app_y + (app_height // 2) - (dialog_height // 2)

        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")

    def load_selected_config(self):
        selected_index = self.config_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a config file.")
            return

        selected_file = self.config_listbox.get(selected_index)
        file_path = os.path.join(settings.CONFIG_FOLDER, selected_file)
        self.app.load_config(file_path)
        self.app.update_widgets()
        self.dialog.destroy()
