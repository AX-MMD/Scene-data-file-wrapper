import tkinter as tk
import typing
from tkinter import messagebox

from kk_plap_generator.gui import info_text
from kk_plap_generator.gui.main_menu import ValidationError
from kk_plap_generator.gui.output_mesage_box import CustomMessageBox
from kk_plap_generator.gui.validators import validate_time
from kk_plap_generator.gui.widgets.base import PlapWidget
from kk_plap_generator.gui.widgets.ref_switcher_widget import RefSwitcherWidget

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class RefInterpolableWidget(PlapWidget):
    def __init__(self, app: "PlapUI", masterframe):
        super().__init__(app, masterframe)

        self.ref_keyframe_time_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.ref_keyframe_time_frame.grid(row=1, column=0, sticky="nsew")

        # Top
        self.top_frame = tk.Frame(self.ref_keyframe_time_frame)
        self.top_frame.pack(fill=tk.X)

        self.top_left_frame = tk.Frame(self.top_frame)
        self.top_left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ref_keyframe_time_label = tk.Label(
            self.top_left_frame,
            text="Reference Interpolable",
        )
        self.ref_keyframe_time_label.pack()

        # Interpolable Path
        self.path_frame = tk.Frame(self.ref_keyframe_time_frame)
        self.path_frame.pack(fill=tk.X, padx=5, pady=5)
        self.path_label = tk.Label(self.path_frame, text="Path")
        self.path_label.pack(side=tk.LEFT)
        self.interpolable_path_entry = tk.Entry(self.path_frame)
        self.interpolable_path_entry.insert(0, self.app.store["interpolable_path"])
        self.interpolable_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.interpolable_path_entry.bind("<FocusOut>", self.on_focus_out)

        # Reference keyframe Time
        self.time_frame = tk.Frame(self.ref_keyframe_time_frame)
        self.time_frame.pack(fill=tk.X, padx=5, pady=5)
        self.time_label = tk.Label(self.time_frame, text="Time")
        self.time_label.pack(side=tk.LEFT)
        self.ref_keyframe_time_entry = tk.Entry(self.time_frame, justify="center")
        self.ref_keyframe_time_entry.insert(0, self.app.store["ref_keyframe_time"])
        self.ref_keyframe_time_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ref_keyframe_time_entry.bind("<FocusOut>", self.on_focus_out)
        self.time_format_label = tk.Label(self.time_frame, text="MM:SS.SS")
        self.time_format_label.pack(side=tk.RIGHT)

        # Buttons for plap_group
        self.ref_switcher_widget = RefSwitcherWidget(app, self.ref_keyframe_time_frame)

        # README
        self.readme_frame = tk.Frame(self.ref_keyframe_time_frame)
        self.readme_frame.pack(fill=tk.X, padx=5, pady=15)
        info_message = info_text.README

        def show_info():
            CustomMessageBox(self.readme_frame, "README", info_message)

        self.info_button = tk.Button(
            self.readme_frame, text="README", fg="red", command=show_info
        )
        self.info_button.pack(fill=tk.X)

    def update(self):
        self.ref_keyframe_time_entry.delete(0, tk.END)
        self.ref_keyframe_time_entry.insert(0, self.app.store["ref_keyframe_time"])
        self.interpolable_path_entry.delete(0, tk.END)
        self.interpolable_path_entry.insert(0, self.app.store["interpolable_path"])

    def on_focus_out(self, event):
        try:
            self.save()
        except ValidationError as e:
            messagebox.showerror("ValidationError", e.get_err_str())

    def save(self):
        errors = []
        ref_keyframe_time = self.ref_keyframe_time_entry.get()
        if len(ref_keyframe_time.split(".")) < 2:
            ref_keyframe_time += ".00"
        if not validate_time(ref_keyframe_time):
            errors.append("Invalid ref_keyframe_time format. Expected MM:SS.SS")
            self.ref_keyframe_time_entry.delete(0, tk.END)
            self.ref_keyframe_time_entry.insert(0, self.app.store["ref_keyframe_time"])
        else:
            self.app.store["ref_keyframe_time"] = ref_keyframe_time

        if errors:
            raise ValidationError(errors=errors)

        self.app.store["interpolable_path"] = self.interpolable_path_entry.get()

        return super().save()
