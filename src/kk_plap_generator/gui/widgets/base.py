from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tkinter as tk

    from kk_plap_generator.gui.main_menu import PlapUI


class PlapWidget:
    def __init__(self, app: "PlapUI", masterframe: "tk.Frame"):
        self.app = app
        self.masterframe = masterframe
        self.app.widgets.append(self)

    def update(self):
        return

    def save(self):
        return
