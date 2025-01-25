import tkinter as tk
import typing

from kk_plap_generator.plap_generator import PlapGenerator

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI

class SoundPatternWidget:
    def __init__(self, app: 'PlapUI', masterframe):
        self.app = app
        self.masterframe = masterframe
        self.store = app.store

        app.pattern_string_frame = tk.Frame(masterframe, bd=2, relief="solid")
        app.pattern_string_frame.grid(row=1, column=0, sticky="nsew")
        app.pattern_string_label = tk.Label(
            app.pattern_string_frame, text="Sound Pattern"
        )
        app.pattern_string_label.pack()
        app.pattern_string_value = tk.Label(
            app.pattern_string_frame,
            text=self.store["pattern_string"],
        )
        app.pattern_string_value.pack()

        app.pattern_buttons_frame = tk.Frame(app.pattern_string_frame)
        app.pattern_buttons_frame.pack()
        for char in PlapGenerator.VALID_PATTERN_CHARS:

            def button_action(c=char):
                self.add_to_pattern_string(c)

            button = tk.Button(
                app.pattern_buttons_frame,
                text=char,
                command=button_action,
            )
            button.pack(side=tk.LEFT)

        app.clear_pattern_string_button = tk.Button(
            app.pattern_string_frame, text="Clear", command=self.clear_pattern_string
        )
        app.clear_pattern_string_button.pack()

    def add_to_pattern_string(self, char):
        self.store["pattern_string"] += char
        self.app.pattern_string_value.config(
            text=self.store["pattern_string"]
        )

    def clear_pattern_string(self):
        self.store["pattern_string"] = ""
        self.app.pattern_string_value.config(text="")

    def update(self):
        self.app.pattern_string_value.config(
            text=self.store["pattern_string"]
        )

    def save(self):
        errors = []
        if not self.store.get("pattern_string"):
            self.store["pattern_string"] = PlapGenerator.VALID_PATTERN_CHARS[0]

        return errors