import tkinter as tk
import typing
from tkinter import messagebox

from kk_plap_generator.gui.validators import ValidationError
from kk_plap_generator.gui.widgets.base import PlapWidget
from kk_plap_generator.utils import load_config_file

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class RefSwitcherWidget(PlapWidget):
    def __init__(self, app: "PlapUI", masterframe):
        super().__init__(app, masterframe)

        self.button_frame = tk.Frame(masterframe)
        self.button_frame.pack(fill=tk.X, padx=(20, 5), pady=5)
        self.create_plap_group_buttons()

    def create_plap_group_buttons(self):
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Create buttons for plap_group
        for i, _ in enumerate(self.app.plap_config):
            if i >= 5:
                break

            def update_current_page(i=i):
                self.update_current_page(i)

            button = tk.Button(
                self.button_frame,
                text=str(i + 1),
                command=update_current_page,
                bg="lightblue" if i == self.app.current_page else "SystemButtonFace",
            )
            button.pack(side=tk.LEFT, padx=5)

        # Reset Button
        reset_button = tk.Button(
            self.button_frame,
            text="⟲",
            font=self.app.symbol_font,
            command=self.reset_button_action,
        )
        reset_button.pack(side=tk.RIGHT)
        delete_button = tk.Button(
            self.button_frame,
            text="✖",
            fg="red",
            font=self.app.symbol_font,
            command=self.delete_plap_group,
        )
        delete_button.pack(side=tk.RIGHT)
        # Add + and delete buttons
        add_button = tk.Button(
            self.button_frame,
            text="✚",
            fg="green",
            font=self.app.symbol_font,
            command=self.add_plap_group,
        )
        add_button.pack(side=tk.RIGHT, padx=(0, 0))

    def update_current_page(self, page_number):
        self.app.current_page = page_number
        self.create_plap_group_buttons()
        self.app.update_widgets()

    def add_plap_group(self):
        try:
            self.app.widgets_save()
            if len(self.app.plap_config) < 5:
                default_entry = load_config_file(self.app.default_config_path)[
                    "plap_group"
                ][0]
                default_entry["interpolable_path"] = self.app.store["interpolable_path"]
                self.app.plap_config.append(default_entry)
                self.app.current_page = len(self.app.plap_config) - 1
                self.create_plap_group_buttons()
                self.app.update_widgets()
        except ValidationError as e:
            messagebox.showerror("ValidationError", e.get_err_str())

    def delete_plap_group(self):
        try:
            self.app.widgets_save()
            if len(self.app.plap_config) > 1:
                self.app.plap_config.pop(self.app.current_page)
                self.app.current_page = min(
                    self.app.current_page, len(self.app.plap_config) - 1
                )
                self.create_plap_group_buttons()
                self.app.update_widgets()
        except ValidationError as e:
            messagebox.showerror("ValidationError", e.get_err_str())

    def reset_button_action(self):
        default_entry = load_config_file(self.app.default_config_path)["plap_group"][0]
        default_entry["interpolable_path"] = self.app.store["interpolable_path"]
        default_entry["ref_keyframe_time"] = self.app.store["ref_keyframe_time"]
        self.app.store.update(default_entry)
        self.app.update_widgets()

    def update(self):
        self.create_plap_group_buttons()
