import tkinter as tk


class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("640x300")  # Set the initial size of the message box

        self.message_frame = tk.Frame(self)
        self.message_frame.pack(fill=tk.BOTH, expand=True)

        self.text = tk.Text(self.message_frame, wrap=tk.WORD)
        self.text.insert(tk.END, message)
        self.text.config(state=tk.DISABLED, padx=10, pady=10)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.message_frame, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)

        self.ok_button = tk.Button(self, text="✖", command=self.destroy)
        self.ok_button.pack(pady=10)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
