import os
import itertools
import sys

import tkinter as tk
from lib import set_wallpaper


class WallpaperManager:
    def __init__(self):
        self.folder = ""
        self.images = []
        self.cycle = None
        self.slideshow_enabled = False

    def _load_images(self, folder: str):
        if not folder or not os.path.isdir(self.folder):
            return []
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        files = []
        for name in os.listdir(folder):
            if os.path.splitext(name)[1].lower() not in valid_extensions:
                continue
            files.append(os.path.join(folder, name))
        return files

    def set_folder(self, folder: str):
        self.folder = folder
        self.images = self._load_images(folder)
        if self.images:
            self.cycle = itertools.cycle(self.images)
        else:
            self.cycle = None

    def next_wallpaper(self):
        if not self.cycle:
            return None
        path = next(self.cycle)
        set_wallpaper(path)
        return path


class App:
    def __init__(self, _root: tk.Tk, interval_seconds: int):
        self.root = _root
        self.root.title("Wallpaper Changer")
        self.manager = WallpaperManager()

        self.folder_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.interval_seconds = interval_seconds

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill="x")

        lbl = tk.Label(frame, text="Wallpaper folder:")
        lbl.grid(row=0, column=0, sticky="w")

        entry = tk.Entry(frame, textvariable=self.folder_var)
        entry.grid(row=1, column=0, sticky="we")

        browse_btn = tk.Button(frame, text="Browse...")
        browse_btn.grid(row=1, column=1, sticky="w")

        frame.grid_columnconfigure(0, weight=1)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(padx=10, pady=(0, 10), fill="x")

        start_btn = tk.Button(btn_frame, text="Start slideshow")
        start_btn.pack(side="left")

        stop_btn = tk.Button(btn_frame, text="Stop slideshow")
        stop_btn.pack(side="left", padx=5)

        next_btn = tk.Button(btn_frame, text="Next now")
        next_btn.pack(side="left", padx=5)

        status_lbl = tk.Label(self.root, textvariable=self.status_var)
        status_lbl.pack(fill="x", padx=10, pady=(0, 5))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, 10)
    root.mainloop()
