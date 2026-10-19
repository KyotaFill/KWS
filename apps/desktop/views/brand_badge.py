"""A transparent brand mark that blends into its surrounding surface."""

import tkinter as tk
from importlib.resources import as_file, files

from PIL import Image, ImageOps, ImageTk


class BrandBadge(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, highlightthickness=0, borderwidth=0)
        with as_file(files("apps.desktop.assets").joinpath("kws-logo-monochrome.png")) as path:
            with Image.open(path) as source:
                mark = source.convert("RGBA")
                # Size the visible mark, rather than its transparent export margins.
                bounds = mark.getchannel("A").point(lambda alpha: 255 if alpha > 8 else 0).getbbox()
                self.source = mark.crop(bounds)
        self.set_palette("#515154", compact=False)

    def set_palette(self, background, *, compact):
        size = 48 if compact else 60
        self.configure(width=size, height=size, background=background)
        self.delete("all")
        # Use one silhouette for both themes so its contours never change.
        red, green, blue = self.winfo_rgb(background)
        light = (.2126 * red + .7152 * green + .0722 * blue) / 65535 > .6
        mark = Image.new("RGBA", self.source.size, "#103b63" if light else "#ffffff")
        mark.putalpha(self.source.getchannel("A"))
        self.photo = ImageTk.PhotoImage(
            ImageOps.contain(mark, (size-4, size-4), Image.Resampling.LANCZOS),
            master=self,
        )
        self.create_image(size/2, size/2, image=self.photo)

    def destroy(self):
        self.photo = None
        super().destroy()
