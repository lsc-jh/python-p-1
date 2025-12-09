import os
import itertools
import sys

import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image
import pystray
from pystray import MenuItem as item

from lib import set_wallpaper

INTERVAL_SECONDS = 60
IS_MAC = sys.platform == "darwin"


class WallpaperManager:
    def __init__(self):
        self.folder = ""
        self.images = []
        self.cycle = None
        self.slideshow_enabled = False

    def set_folder(self, folder: str):
        """Set the folder and reload images."""
        self.folder = folder
        self.images = self._load_images(folder)
        if self.images:
            self.cycle = itertools.cycle(self.images)
        else:
            self.cycle = None

    def _load_images(self, folder):
        if not folder or not os.path.isdir(folder):
            return []
        exts = {".jpg", ".jpeg", ".png", ".bmp"}
        files = []
        for name in os.listdir(folder):
            if os.path.splitext(name)[1].lower() in exts:
                files.append(os.path.join(folder, name))
        return files

    def next_wallpaper(self):
        """Switch to the next wallpaper in the folder."""
        if not self.cycle:
            return
        path = next(self.cycle)
        set_wallpaper(path)
        return path  # useful for status messages


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Wallpaper Changer")
        self.manager = WallpaperManager()

        # UI state
        self.folder_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Select a folder to start.")
        self.interval_seconds = INTERVAL_SECONDS

        # Build UI
        self._build_ui()

        # Slideshow loop (handled via Tk's after)
        self._slideshow_scheduled = False

        # Tray icon
        self.tray_icon = None
        self._start_tray_icon()

    def _build_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill="x")

        lbl = tk.Label(frame, text="Wallpaper folder:")
        lbl.grid(row=0, column=0, sticky="w")

        entry = tk.Entry(frame, textvariable=self.folder_var, width=40)
        entry.grid(row=1, column=0, sticky="we", padx=(0, 5))

        browse_btn = tk.Button(frame, text="Browse...", command=self.browse_folder)
        browse_btn.grid(row=1, column=1)

        frame.grid_columnconfigure(0, weight=1)

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(padx=10, pady=(0, 10), fill="x")

        start_btn = tk.Button(buttons_frame, text="Start slideshow", command=self.start_slideshow)
        start_btn.pack(side="left")

        stop_btn = tk.Button(buttons_frame, text="Stop slideshow", command=self.stop_slideshow)
        stop_btn.pack(side="left", padx=5)

        next_btn = tk.Button(buttons_frame, text="Next now", command=self.next_now)
        next_btn.pack(side="left", padx=5)

        status_label = tk.Label(self.root, textvariable=self.status_var, anchor="w")
        status_label.pack(fill="x", padx=10, pady=(0, 5))

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select wallpaper folder")
        if not folder:
            return
        self.folder_var.set(folder)
        self.manager.set_folder(folder)
        if self.manager.images:
            self.status_var.set(f"Loaded {len(self.manager.images)} images.")
        else:
            self.status_var.set("No images found in that folder.")

    def start_slideshow(self):
        if not self.manager.images:
            messagebox.showwarning("No images", "Please select a folder with images first.")
            return
        self.manager.slideshow_enabled = True
        self.status_var.set("Slideshow started.")
        if not self._slideshow_scheduled:
            self._schedule_slideshow_step()

    def stop_slideshow(self):
        self.manager.slideshow_enabled = False
        self.status_var.set("Slideshow stopped.")

    def next_now(self):
        if not self.manager.images:
            messagebox.showwarning("No images", "Please select a folder with images first.")
            return
        path = self.manager.next_wallpaper()
        if path:
            self.status_var.set(f"Set wallpaper: {os.path.basename(path)}")

    def _schedule_slideshow_step(self):
        """Schedule the periodic wallpaper change with Tk's event loop."""
        self._slideshow_scheduled = True

        def step():
            # This runs in Tk's thread
            if self.manager.slideshow_enabled and self.manager.images:
                path = self.manager.next_wallpaper()
                if path:
                    self.status_var.set(f"Slideshow: {os.path.basename(path)}")
            # Schedule next call if slideshow is still enabled
            if self.manager.slideshow_enabled:
                self.root.after(self.interval_seconds * 1000, step)
            else:
                self._slideshow_scheduled = False

        self.root.after(self.interval_seconds * 1000, step)

    def _start_tray_icon(self):
        """Start the system tray icon (must be created on the main thread on macOS)."""
        self.root.after(0, self._create_tray_icon)

    def _create_tray_icon(self):
        image = Image.new("RGB", (16, 16), "black")

        menu = pystray.Menu(
            item("Start slideshow", self._tray_start_slideshow),
            item("Stop slideshow", self._tray_stop_slideshow),
            item("Next now", self._tray_next_now),
            item("Quit", self._tray_quit),
        )

        self.tray_icon = pystray.Icon("wallpaper_tray", image, "Wallpaper changer", menu)
        self.tray_icon.run_detached()

    def _tray_start_slideshow(self, icon, menu_item):
        if not self.manager.images:
            return

        def start():
            self.manager.slideshow_enabled = True
            if not self._slideshow_scheduled:
                self._schedule_slideshow_step()
            self.status_var.set("Slideshow started (from tray).")

        self.root.after(0, start)

    def _tray_stop_slideshow(self, icon, menu_item):
        def stop():
            self.manager.slideshow_enabled = False
            self.status_var.set("Slideshow stopped (from tray).")

        self.root.after(0, stop)

    def _tray_next_now(self, icon, menu_item):
        if not self.manager.images:
            return

        def next_step():
            path = self.manager.next_wallpaper()
            if path:
                self.status_var.set(f"Set wallpaper (tray): {os.path.basename(path)}")

        self.root.after(0, next_step)

    def _tray_quit(self, icon, menu_item):
        icon.stop()

        def quit_app():
            self.root.quit()
            self.root.destroy()
            os._exit(0)

        self.root.after(0, quit_app)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
