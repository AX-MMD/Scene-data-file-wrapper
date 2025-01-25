import tkinter as tk
from tkinter import messagebox
import typing

if typing.TYPE_CHECKING:
    from kk_plap_generator.gui.main_menu import PlapUI

class TimeRangesWidget:
    def __init__(self, app: "PlapUI", masterframe):
        self.app = app
        self.masterframe = masterframe
        self.store = app.store

        app.time_ranges_frame = tk.Frame(masterframe, bd=2, relief="solid")
        app.time_ranges_frame.grid(row=1, column=0, sticky="nsew")
        app.time_ranges_label = tk.Label(app.time_ranges_frame, text="Time Ranges")
        app.time_ranges_label.pack()

        app.time_ranges_listbox = tk.Listbox(app.time_ranges_frame)
        app.time_ranges_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        app.time_ranges_scrollbar = tk.Scrollbar(
            app.time_ranges_frame, orient="vertical"
        )
        app.time_ranges_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        app.time_ranges_listbox.config(yscrollcommand=app.time_ranges_scrollbar.set)
        app.time_ranges_scrollbar.config(command=app.time_ranges_listbox.yview)

        self.update()

        app.add_time_range_button = tk.Button(
            app.time_ranges_frame, text="+", command=self.add_time_range
        )
        app.add_time_range_button.pack(fill=tk.X)

        app.remove_time_range_button = tk.Button(
            app.time_ranges_frame, text="-", command=self.remove_selected_time_range
        )
        app.remove_time_range_button.pack(fill=tk.X)

    def update(self):
        self.app.time_ranges_listbox.delete(0, tk.END)
        for start, stop in self.store.get("time_ranges", []):
            self.app.time_ranges_listbox.insert(tk.END, f"{start} - {stop}")

    def remove_selected_time_range(self):
        selected_index = self.time_ranges_listbox.curselection()
        if selected_index:
            selected_time_range = self.time_ranges_listbox.get(selected_index)
            start, stop = selected_time_range.split(" - ")
            self.store["time_ranges"].remove([start, stop])
            self.update_time_ranges()        

    def add_time_range(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Add Time Range")

        tk.Label(dialog, text="Start Time").grid(row=0, column=0)
        start_time_entry = tk.Entry(dialog, justify="center")
        start_time_entry.grid(row=0, column=1)
        start_time_entry.insert(0, "00:00.00")
        tk.Label(dialog, text="MM:SS.SS").grid(row=0, column=2)

        tk.Label(dialog, text="Stop Time").grid(row=1, column=0)
        stop_time_entry = tk.Entry(dialog, justify="center")
        stop_time_entry.grid(row=1, column=1)
        stop_time_entry.insert(0, "00:00.00")
        tk.Label(dialog, text="MM:SS.SS").grid(row=1, column=2)

        def on_ok():
            start_time = start_time_entry.get()
            stop_time = stop_time_entry.get()
            if not self.validate_time(start_time) and self.validate_time(stop_time):
                messagebox.showerror(
                    "Validation Error", "Invalid time format. Expected MM:SS.SS"
                )
            elif start_time > stop_time:
                messagebox.showerror(
                    "Validation Error", "Start time must be before Stop time"
                )
            else:
                self.store["time_ranges"].append(
                    [start_time, stop_time]
                )
                self.update_time_ranges()
                dialog.destroy()

        tk.Button(dialog, text="Ok", command=on_ok).grid(row=2, column=0, columnspan=3)