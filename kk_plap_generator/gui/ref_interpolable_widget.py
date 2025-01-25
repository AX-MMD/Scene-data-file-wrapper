import tkinter as tk
import typing

from kk_plap_generator.gui.validators import validate_offset, validate_time

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class RefInterpolableWidget:
    def __init__(self, app: "PlapUI", masterframe):
        self.app = app
        self.masterframe = masterframe
        self.store = app.store

        self.ref_keyframe_time_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.ref_keyframe_time_frame.grid(row=1, column=0, sticky="nsew")
        self.ref_keyframe_time_label = tk.Label(
            self.ref_keyframe_time_frame, text="Reference Interpolable"
        )
        self.ref_keyframe_time_label.pack()

        self.time_frame = tk.Frame(self.ref_keyframe_time_frame)
        self.time_frame.pack(fill=tk.X, padx=5, pady=5)
        self.time_label = tk.Label(self.time_frame, text="Time")
        self.time_label.pack(side=tk.LEFT)
        self.ref_keyframe_time_entry = tk.Entry(self.time_frame, justify="center")
        self.ref_keyframe_time_entry.insert(
            0, self.store["ref_keyframe_time"]
        )
        self.ref_keyframe_time_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.time_format_label = tk.Label(self.time_frame, text="MM:SS.SS")
        self.time_format_label.pack(side=tk.RIGHT)

        self.path_frame = tk.Frame(self.ref_keyframe_time_frame)
        self.path_frame.pack(fill=tk.X, padx=5, pady=5)
        self.path_label = tk.Label(self.path_frame, text="Path")
        self.path_label.pack(side=tk.LEFT)
        self.interpolable_path_entry = tk.Entry(self.path_frame)
        self.interpolable_path_entry.insert(
            0, self.store["interpolable_path"]
        )
        self.interpolable_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update(self):
        self.ref_keyframe_time_entry.delete(0, tk.END)
        self.ref_keyframe_time_entry.insert(
            0, self.store["ref_keyframe_time"]
        )
        self.interpolable_path_entry.delete(0, tk.END)
        self.interpolable_path_entry.insert(
            0, self.store['interpolable_path']
        )

    def save(self):
        errors = []
        ref_keyframe_time = self.ref_keyframe_time_entry.get()
        if len(ref_keyframe_time.split(".")) < 2:
            ref_keyframe_time += ".00"
        if not validate_time(ref_keyframe_time):
            errors.append("Invalid ref_keyframe_time format. Expected MM:SS.SS")
            self.ref_keyframe_time_entry.delete(0, tk.END)
            self.ref_keyframe_time_entry.insert(
                0, self.store["ref_keyframe_time"]
            )
        else:
            self.store["ref_keyframe_time"] = ref_keyframe_time

        self.store["interpolable_path"] = (
            self.interpolable_path_entry.get()
        )

        return errors
    