import tkinter as tk
import typing

from kk_plap_generator.gui.info_message import InfoMessageFrame
from kk_plap_generator.gui.validators import validate_offset

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class SeqAdjustmentWidget:
    def __init__(self, app: "PlapUI", masterframe):
        self.app = app
        self.masterframe = masterframe

        self.offset_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.offset_frame.grid(row=0, column=0, sticky="nsew")

        # Top
        self.top_frame = tk.Frame(self.offset_frame)
        self.top_frame.grid_columnconfigure(0, weight=90)
        self.top_frame.grid_columnconfigure(1, weight=10)
        self.top_frame.pack(fill=tk.X)

        # Offset
        self.top_left_frame = tk.Frame(self.top_frame)
        self.top_left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.offset_label = tk.Label(self.top_left_frame, text="Sound Offset")
        self.offset_label.pack()
        self.offset_entry = tk.Entry(self.offset_frame, justify="center")
        self.offset_entry.insert(0, self.app.store["offset"])
        self.offset_entry.pack()

        info_message = """
[---------------------------- Adjustments ---------------------------]

These settings are only used for corrections, only change them if there is to much plaps, not enough plaps, or the plaps are not synced with the reference.

::: Offset :::
Offset in seconds, in case you don't want the sfx to be timed exactly with the reference keyframes. Can be positive or negative.

::: Minimum Pull Out % :::
The generator estimates the distance traveled by the subject for each plap, here you can set what (%) of that distance the subject needs to pull away from the contact point before re-enabling plaps.

This is to prevents spam if the subject is making micro in-out moves when fully inserted.

::: Minimum Push In % :::
The generator estimates the distance traveled by the subject for each plap, here you can set what (%) of that distance the subject needs to push toward the contact point for a plap to register.

This is in case the contact point gets closer and the subject does not need to thrust as far.
        """
        self.top_right_frame = InfoMessageFrame(self.top_frame, info_message)

        # Min Pull Out
        self.min_pull_out_label = tk.Label(self.offset_frame, text="Minimum Pull Out %")
        self.min_pull_out_label.pack()
        self.min_pull_out_frame = tk.Frame(self.offset_frame)
        self.min_pull_out_frame.pack()
        # Slider
        self.min_pull_out_slider = tk.Scale(
            self.min_pull_out_frame, from_=0, to=100, orient=tk.HORIZONTAL, resolution=0.5
        )
        self.min_pull_out_slider.set(self.app.store["min_pull_out"] * 100)

        # Left button
        self.min_pull_out_left_button = tk.Button(
            self.min_pull_out_frame,
            text="<",
            command=lambda: self.adjust_slider(self.min_pull_out_slider, -0.5),
            height=1,
        )

        # Right button
        self.min_pull_out_right_button = tk.Button(
            self.min_pull_out_frame,
            text=">",
            command=lambda: self.adjust_slider(self.min_pull_out_slider, 0.5),
            height=1,
        )

        self.min_pull_out_left_button.pack(side=tk.LEFT)
        self.min_pull_out_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.min_pull_out_right_button.pack(side=tk.LEFT)

        # Min Push In
        self.min_push_in_label = tk.Label(self.offset_frame, text="Minimum Push In %")
        self.min_push_in_label.pack()
        self.min_push_in_frame = tk.Frame(self.offset_frame)
        self.min_push_in_frame.pack()
        # Slider
        self.min_push_in_slider = tk.Scale(
            self.min_push_in_frame, from_=0, to=100, orient=tk.HORIZONTAL, resolution=0.5
        )
        self.min_push_in_slider.set(self.app.store["min_push_in"] * 100)

        # Left button
        self.min_push_in_left_button = tk.Button(
            self.min_push_in_frame,
            text="<",
            command=lambda: self.adjust_slider(self.min_push_in_slider, -0.5),
            height=1,
        )

        # Right button
        self.min_push_in_right_button = tk.Button(
            self.min_push_in_frame,
            text=">",
            command=lambda: self.adjust_slider(self.min_push_in_slider, 0.5),
            height=1,
        )

        self.min_push_in_left_button.pack(side=tk.LEFT, fill=tk.X)
        self.min_push_in_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.min_push_in_right_button.pack(side=tk.LEFT)

    def adjust_slider(self, slider, increment):
        current_value = slider.get()
        new_value = current_value + increment
        if 0 <= new_value <= 100:
            slider.set(new_value)

    def update(self):
        self.offset_entry.delete(0, tk.END)
        self.offset_entry.insert(0, self.app.store["offset"])

        self.min_pull_out_slider.set(self.app.store["min_pull_out"] * 100)
        self.min_push_in_slider.set(self.app.store["min_push_in"] * 100)

    def save(self):
        errors = []
        offset = self.offset_entry.get()
        if not validate_offset(offset):
            errors.append("Invalid offset format. Expected a decimal compatible value")
            self.offset_entry.delete(0, tk.END)
            self.offset_entry.insert(0, self.app.store.get("offset", ""))
        else:
            self.app.store["offset"] = float(offset)

        self.app.store["min_pull_out"] = self.min_pull_out_slider.get() / 100
        self.app.store["min_push_in"] = self.min_push_in_slider.get() / 100

        return errors
