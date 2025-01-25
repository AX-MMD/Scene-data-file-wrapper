import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import toml
import tkinterdnd2

from kk_plap_generator import settings
from kk_plap_generator.gui.dnd_widget import DnDWidget
from kk_plap_generator.gui.ref_interpolable_widget import RefInterpolableWidget
from kk_plap_generator.gui.seq_adjustment_widget import SeqAdjustmentWidget
from kk_plap_generator.gui.sound_folders_widget import SoundFoldersWidget
from kk_plap_generator.gui.sound_pattern_widget import SoundPatternWidget
from kk_plap_generator.gui.time_ranges_widget import TimeRangesWidget
from kk_plap_generator.gui.validators import validate_offset, validate_time
from kk_plap_generator.plap_generator import PlapGenerator


class PlapUI(tk.Frame):
    def __init__(self, master=None, config_path=settings.CONFIG_FILE):
        super().__init__(master)
        self.master = master
        self.single_file = None
        self.config_path: str = config_path
        self.plap_config = self.load_config()
        self.store = self.plap_config.get("plap_group")[0]
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def load_config(self):
        with open(self.config_path, "r") as f:
            return toml.load(f)

    def save_button_action(self):
        self.save_config()
        self.load_config()
        self.update_widgets()

    def save_config(self):
        errors = []

        errors.extend(self.ref_interpolable_widget.save())
        errors.extend(self.seq_adjustment_widget.save())
        errors.extend(self.sound_pattern_widget.save())

        if errors:
            messagebox.showerror("Error", "\n".join(errors))
            return

        self.plap_config["plap_group"] = [self.store]

        with open(self.config_path, "w") as f:
            toml.dump(self.plap_config, f)

    def update_widgets(self):
        self.ref_interpolable_widget.update()
        self.seq_adjustment_widget.update()
        self.sound_folders_widget.update()
        self.time_ranges_widget.update()

    def create_widgets(self):
        # Create the main 1x3 grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left frame with 2x1 grid
        self.left_frame = tk.Frame(self)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.grid_rowconfigure(0, weight=2)
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Middle frame with 2x1 grid
        self.middle_frame = tk.Frame(self)
        self.middle_frame.grid(row=0, column=1, sticky="nsew")
        self.middle_frame.grid_rowconfigure(0, weight=1)
        self.middle_frame.grid_rowconfigure(1, weight=1)
        self.middle_frame.grid_columnconfigure(0, weight=1)

        # Right frame with 2x1 grid
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=2, sticky="nsew")
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Drop file
        self.dnd_widget = DnDWidget(self, self.left_frame)

        # Reference Interpolable
        self.ref_interpolable_widget = RefInterpolableWidget(self, self.left_frame)

        # Sound Folder Names
        self.sound_folders_widget = SoundFoldersWidget(self, self.middle_frame)

        # Sound Pattern
        self.sound_pattern_widget = SoundPatternWidget(self, self.middle_frame)

        # Save Button
        self.save_button = tk.Button(self, text="Save", command=self.save_button_action)
        self.save_button.grid(row=2, column=1, sticky="nsew")

        # Sound Offset and Min Pull Out/In
        self.seq_adjustment_widget = SeqAdjustmentWidget(self, self.right_frame)

        # Time Ranges
        self.time_ranges_widget = TimeRangesWidget(self, self.right_frame)

    @classmethod
    def default_config(cls) -> tkinterdnd2.Tk:
        root = tkinterdnd2.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = max(640, min(854, screen_width // 3))
        window_height = max(360, min(480, screen_height // 3))
        root.geometry(f"{window_width}x{window_height}")
        return root
    
    @classmethod
    def run(cls):
        app = cls(master=cls.default_config())
        app.mainloop()
