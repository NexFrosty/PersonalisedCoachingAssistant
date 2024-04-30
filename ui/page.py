import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk


class Page(ctk.CTkFrame):
    fg_color1 = "#221f1f"
    fg_color2 = "#252323"

    def __init__(self, parent, bg_image=None, **kwargs):
        super().__init__(parent)
        self.parent = parent
        if bg_image is not None:
            if type(bg_image) == str:
                self.add_background_from_file(bg_image)
            else:
                self.add_background(bg_image)
        self._set_data(**kwargs)

    def _resize_bg_image(self, event):
        nw = event.width
        nh = event.height
        self.bg_image.configure(size=(nw, nh))

    def _set_data(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_background_from_file(self, bg_image):
        self.image = Image.open(bg_image)
        self.add_background(self.image)

    def add_background(self, bg_image):
        self.bg_image = ctk.CTkImage(dark_image=bg_image, size=bg_image.size)
        self.bg = ctk.CTkLabel(self, text="", image=self.bg_image)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg.bind("<Configure>", self._resize_bg_image)
