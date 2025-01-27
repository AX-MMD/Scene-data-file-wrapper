import tkinter as tk
import typing
from tkinter import simpledialog

from kk_plap_generator.gui.info_message import InfoMessageFrame
from kk_plap_generator.gui.validators import validate_time

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI


class TimeRangesWidget:
    def __init__(self, app: "PlapUI", masterframe):
        self.app = app
        self.masterframe = masterframe

        self.time_ranges_frame = tk.Frame(masterframe, bd=2, relief="solid")
        self.time_ranges_frame.grid(row=1, column=0, sticky="nsew")

        # Top
        self.top_frame = tk.Frame(self.time_ranges_frame)
        self.top_frame.grid_columnconfigure(0, weight=90)
        self.top_frame.grid_columnconfigure(1, weight=10)
        self.top_frame.pack(fill=tk.X)

        # Time Ranges
        self.top_left_frame = tk.Frame(self.top_frame)
        self.top_left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.time_ranges_label = tk.Label(self.top_left_frame, text="Time Ranges")
        self.time_ranges_label.pack()

        info_text = """
        [-------------------------------- Adjustments --------------------------------]

        ::: Time Ranges :::  
        By default the generator will try to make keyframes starting from 00:00.00.
        You can have a different start point, end point or multiple ranges.

        For exemple, if you give the ranges 00:01.5, 00:05.0 and 00:10.5, 00:15.0 the
        generator will try to make keyframes only at those points.

        !!! If you give a custom range, you must put both a Start and Stop point. !!!
        """

        self.top_right_frame = InfoMessageFrame(self.top_frame, info_text)

        self.time_ranges_listbox = tk.Listbox(self.time_ranges_frame)
        self.time_ranges_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.time_ranges_scrollbar = tk.Scrollbar(
            self.time_ranges_frame, orient="vertical"
        )
        self.time_ranges_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.time_ranges_listbox.config(yscrollcommand=self.time_ranges_scrollbar.set)
        self.time_ranges_scrollbar.config(command=self.time_ranges_listbox.yview)

        self.update()

        self.add_time_range_button = tk.Button(
            self.time_ranges_frame, text="+", command=self.add_time_range
        )
        self.add_time_range_button.pack(fill=tk.X)

        self.remove_time_range_button = tk.Button(
            self.time_ranges_frame, text="-", command=self.remove_selected_time_range
        )
        self.remove_time_range_button.pack(fill=tk.X)

    def update(self):
        self.time_ranges_listbox.delete(0, tk.END)
        for start, stop in self.app.store.get("time_ranges", []):
            self.time_ranges_listbox.insert(tk.END, f"{start} - {stop}")

    def remove_selected_time_range(self):
        selected_index = self.time_ranges_listbox.curselection()
        if selected_index:
            selected_time_range = self.time_ranges_listbox.get(selected_index)
            start, stop = selected_time_range.split(" - ")
            self.app.store["time_ranges"].remove([start, stop])
            self.update()

    def add_time_range(self):
        dialog = CustomDialog(self.masterframe, title="Add Time Range")
        result = dialog.result
        if result:
            start_time = result["start_time"]
            stop_time = result["stop_time"]
            if validate_time(start_time) and validate_time(stop_time):
                self.app.store["time_ranges"].append([start_time, stop_time])
                self.update()
            else:
                tk.messagebox.showerror(
                    "Validation Error", "Invalid time format. Expected MM:SS.SS"
                )


class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.ok_text = "✔"
        self.cancel_text = "✖"
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Start Time").grid(row=0, column=0)
        self.start_time_entry = tk.Entry(master, justify="center")
        self.start_time_entry.grid(row=0, column=1)
        self.start_time_entry.insert(0, "00:00.00")
        tk.Label(master, text="MM:SS.SS").grid(row=0, column=2)

        tk.Label(master, text="Stop Time").grid(row=1, column=0)
        self.stop_time_entry = tk.Entry(master, justify="center")
        self.stop_time_entry.grid(row=1, column=1)
        self.stop_time_entry.insert(0, "00:00.00")
        tk.Label(master, text="MM:SS.SS").grid(row=1, column=2)

        return self.start_time_entry  # initial focus

    def buttonbox(self):
        box = tk.Frame(self)

        self.ok_button = tk.Button(
            box,
            text=self.ok_text,
            width=10,
            fg="green",
            command=self.ok,
            default=tk.ACTIVE,
        )
        self.ok_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.cancel_button = tk.Button(
            box, text=self.cancel_text, width=10, fg="red", command=self.cancel
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def apply(self):
        self.result = {
            "start_time": self.start_time_entry.get(),
            "stop_time": self.stop_time_entry.get(),
        }
