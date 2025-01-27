import tkinter as tk
import traceback
from tkinter import font, messagebox

import tkinterdnd2
import toml

from kk_plap_generator import settings
from kk_plap_generator.generator.plap_generator import NodeNotFoundError
from kk_plap_generator.generator.utils import generate_plaps
from kk_plap_generator.gui.dnd_widget import DnDWidget
from kk_plap_generator.gui.output_mesage_box import CustomMessageBox
from kk_plap_generator.gui.ref_interpolable_widget import RefInterpolableWidget
from kk_plap_generator.gui.seq_adjustment_widget import SeqAdjustmentWidget
from kk_plap_generator.gui.sound_folders_widget import SoundFoldersWidget
from kk_plap_generator.gui.sound_pattern_widget import SoundPatternWidget
from kk_plap_generator.gui.time_ranges_widget import TimeRangesWidget


class PlapUI(tk.Frame):
    def __init__(
        self,
        master=None,
        config_path=settings.CONFIG_FILE,
        default_config_path=settings.DEFAULT_CONFIG_FILE,
    ):
        super().__init__(master)
        self.master = master
        self.config_path: str = config_path
        self.default_config_path = default_config_path
        self.plap_config = self.load_config()
        self.store = self.plap_config.get("plap_group")[0]
        self.symbol_font = font.Font(family="Arial", size=13)

        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def load_config(self, use_default=False):
        if use_default:
            with open(self.default_config_path, "r") as f:
                return toml.load(f)
        with open(self.config_path, "r") as f:
            return toml.load(f)

    def update_widgets(self):
        self.ref_interpolable_widget.update()
        self.seq_adjustment_widget.update()
        self.sound_folders_widget.update()
        self.sound_pattern_widget.update()
        self.time_ranges_widget.update()

    def create_widgets(self):
        # Create the main 2x3 grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=90)
        self.grid_rowconfigure(1, weight=10)

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

        # Sound Offset and Min Pull Out/In
        self.seq_adjustment_widget = SeqAdjustmentWidget(self, self.right_frame)

        # Time Ranges
        self.time_ranges_widget = TimeRangesWidget(self, self.right_frame)

        self.bottom_left_frame = tk.Frame(self)
        self.bottom_left_frame.grid(row=1, column=0, sticky="nsew")
        self.bottom_left_frame.grid_columnconfigure(0, weight=1)
        self.bottom_left_frame.grid_columnconfigure(1, weight=1)
        self.bottom_left_frame.grid_columnconfigure(2, weight=1)

        # Reset Button
        self.reset_button = tk.Button(
            self.bottom_left_frame, text="Reset ↺", command=self.reset_button_action
        )
        self.reset_button.grid(row=0, column=0, sticky="nsew")

        # Generate Button
        self.generate_button = tk.Button(
            self.bottom_left_frame, text="▶", command=self.generate_plaps
        )
        self.generate_button.grid(row=0, column=1, sticky="nsew")

        # Save Button
        self.save_button = tk.Button(
            self.bottom_left_frame, text="Save 💾", command=self.save_button_action
        )
        self.save_button.grid(row=0, column=2, sticky="nsew")

    def reset_button_action(self):
        self.plap_config = self.load_config(use_default=True)
        self.store = self.plap_config.get("plap_group")[0]
        self.update_widgets()
        self.dnd_widget.reset_single_file()

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

    def generate_plaps(self):
        if self.dnd_widget.get_single_file() is None:
            messagebox.showerror("Error", "Please select a file.xml")
        else:
            try:
                self.save_config()
                output = generate_plaps(
                    self.dnd_widget.get_single_file(), self.plap_config["plap_group"]
                )
                CustomMessageBox(
                    self, "Success ✔", "::: Success :::\n\n" + "\n".join(output)
                )
            except NodeNotFoundError as e:
                if e.xml_path is not None:
                    CustomMessageBox(self, "Failled ✖", traceback.format_exc())

                message = "::: Node not found :::\n"
                message += f"\n> Missing node: {e.get_node_string()}"
                if e.node_name == "interpolableGroup":
                    message += f'\n> Could not find the parent group\n    "{e.value}"\n  in the xml file.'
                    message += f'\n> Make sure the path\n    "{self.store["interpolable_path"]}"\n is correct.'
                elif e.node_name == "interpolable":
                    message += f'\n> Could not find the interpolable\n    "{e.value}"\n  in the xml file.'
                    message += f'\n> Make sure you renamed the interpolable to\n    "{self.store["interpolable_path"].split(".")[-1]}"'
                    message += (
                        "\n  in the Timeline, even if that was already the original name."
                    )
                    message += "\n  This is needed so an alias is created."
                else:
                    message += f'\n> Could not find the node\n    "{e.node_name}"\n  in the xml file.'
                CustomMessageBox(self, "Failled ✖", message)
            except Exception:
                CustomMessageBox(self, "Failled ✖", traceback.format_exc())

    @classmethod
    def default_config(cls) -> tkinterdnd2.Tk:
        root = tkinterdnd2.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = max(640, min(854, screen_width // 3))
        window_height = max(360, min(480, screen_height // 3))
        root.title("PLAP Generator")
        root.minsize(600, 360)
        root.geometry(f"{window_width}x{window_height}")
        return root

    @classmethod
    def run(cls):
        app = cls(master=cls.default_config())
        app.mainloop()
