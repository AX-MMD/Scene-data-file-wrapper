import tkinter as tk
import typing

from kk_plap_generator.generator.plap_generator import PlapGenerator

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class SoundPatternWidget:
    def __init__(self, app: "PlapUI", masterframe):
        self.app = app
        self.masterframe = masterframe
        self.store = app.store

        self.pattern_string_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.pattern_string_frame.grid(row=1, column=0, sticky="nsew")
        self.pattern_string_label = tk.Label(
            self.pattern_string_frame, text="Sound Pattern"
        )
        self.pattern_string_label.pack()
        self.pattern_string_value = tk.Label(
            self.pattern_string_frame,
            text=self.store["pattern_string"],
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
            self.pattern_string_frame, text="Clear ✖", fg="red", command=self.clear_pattern_string
        )
        self.clear_pattern_string_button.pack()

    def add_to_pattern_string(self, char):
        self.store["pattern_string"] += char
        self.pattern_string_value.config(text=self.store["pattern_string"])

    def clear_pattern_string(self):
        self.store["pattern_string"] = ""
        self.pattern_string_value.config(text="")

    def update(self):
        self.pattern_string_value.config(text=self.store["pattern_string"])

    def save(self):
        errors: typing.List[str] = []
        if not self.store.get("pattern_string"):
            self.store["pattern_string"] = PlapGenerator.VALID_PATTERN_CHARS[0]

        return errors
