import tkinter as tk
import typing

from kk_plap_generator.generator.plap_generator import PlapGenerator
from kk_plap_generator.gui import info_text
from kk_plap_generator.gui.info_message import InfoMessageFrame
from kk_plap_generator.gui.widgets.base import PlapWidget

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class SoundPatternWidget(PlapWidget):
    def __init__(self, app: "PlapUI", masterframe):
        super().__init__(app, masterframe)

        self.pattern_string_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.pattern_string_frame.grid(row=1, column=0, sticky="nsew")

        # Top
        self.top_frame = tk.Frame(self.pattern_string_frame)
        self.top_frame.grid_columnconfigure(0, weight=90)
        self.top_frame.grid_columnconfigure(1, weight=10)
        self.top_frame.pack(fill=tk.X)

        self.top_left_frame = tk.Frame(self.top_frame)
        self.top_left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pattern_string_label = tk.Label(self.top_left_frame, text="Sound Pattern")
        self.pattern_string_label.pack()

        # The pattern looks bad here but it's good on the display
        info_message = info_text.SOUND_PATTERN
        self.top_right_frame = InfoMessageFrame(self.top_frame, info_message)

        # Pattern value display
        self.pattern_string_value = tk.Label(
            self.pattern_string_frame,
            text=self.app.store["pattern_string"],
        )
        self.pattern_string_value.pack()

        self.pattern_buttons_frame = tk.Frame(self.pattern_string_frame)
        self.pattern_buttons_frame.pack()
        for char in PlapGenerator.VALID_PATTERN_CHARS:

            def button_action(c=char):
                self.add_to_pattern_string(c)

            button = tk.Button(
                self.pattern_buttons_frame,
                text=char,
                command=button_action,
            )
            button.pack(side=tk.LEFT)

        self.clear_pattern_string_button = tk.Button(
            self.pattern_string_frame,
            text="Clear ✖",
            command=self.clear_pattern_string,
        )
        self.clear_pattern_string_button.pack()

    def add_to_pattern_string(self, char):
        self.app.store["pattern_string"] += char
        self.pattern_string_value.config(text=self.app.store["pattern_string"])

    def clear_pattern_string(self):
        self.app.store["pattern_string"] = ""
        self.pattern_string_value.config(text="")

    def update(self):
        self.pattern_string_value.config(text=self.app.store["pattern_string"])

    def save(self):
        if not self.app.store.get("pattern_string"):
            self.app.store["pattern_string"] = PlapGenerator.VALID_PATTERN_CHARS[0]
        return super().save()
