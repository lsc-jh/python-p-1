import tkinter as tk
from tkinter import filedialog, messagebox
from manager import WallpaperManager
import time
from PIL import Image
import pystray
from pystray import MenuItem as Item


class App:
    def __init__(self, _root: tk.Tk, interval_seconds: int):
        self.root = _root
        self.root.title("Wallpaper Changer")
        self.manager = WallpaperManager()

        self.folder_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.timer_var = tk.StringVar()
        self.interval_seconds = interval_seconds

        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.tray_icon = None

        self._build_ui()

        self._start_tray_icon()

    def show_window(self):
        def _show():
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()

        self.root.after(0, _show)

    def hide_window(self):
        def _hide():
            self.root.withdraw()

        self.root.after(0, _hide)

    def _build_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill="x")

        lbl = tk.Label(frame, text="Wallpaper folder:")
        lbl.grid(row=0, column=0, sticky="w")

        entry = tk.Entry(frame, textvariable=self.folder_var)
        entry.grid(row=1, column=0, sticky="we")

        browse_btn = tk.Button(frame, text="Browse...", command=self.browse_folder)
        browse_btn.grid(row=1, column=1, sticky="w")

        frame.grid_columnconfigure(0, weight=1)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(padx=10, pady=(0, 10), fill="x")

        start_btn = tk.Button(btn_frame, text="Start slideshow", command=self.start_slideshow)
        start_btn.pack(side="left")

        stop_btn = tk.Button(btn_frame, text="Stop slideshow", command=self.stop_slideshow)
        stop_btn.pack(side="left", padx=5)

        next_btn = tk.Button(btn_frame, text="Next now", command=self.next_now)
        next_btn.pack(side="left", padx=5)

        status_frame = tk.Frame(self.root)
        status_frame.pack(padx=10, pady=(0, 5), fill="x")

        status_lbl = tk.Label(status_frame, textvariable=self.status_var)
        status_lbl.pack(side="right")

        timer_lbl = tk.Label(status_frame, textvariable=self.timer_var)
        timer_lbl.pack(side="left")

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Wallpaper folder")
        if not folder:
            return
        self.folder_var.set(folder)
        self.manager.set_folder(folder)
        if self.manager.images:
            self.status_var.set(f"Loaded {len(self.manager.images)} images.")
        else:
            self.status_var.set("No images found in the selected folder.")

    def next_now(self):
        if not self.manager.images:
            messagebox.showwarning("no images", "please select a folder with images first.")
            return

        path = self.manager.next_wallpaper()
        if path:
            self.status_var.set(f"Set wallpaper: {path}")

        self._reset_countdown()

    def start_slideshow(self):
        if not self.manager.images:
            messagebox.showwarning("no images", "please select a folder with images first.")
            return
        self.status_var.set("Slideshow started.")
        self._schedule_slideshow_step()

    def stop_slideshow(self):
        self.status_var.set("Slideshow stopped.")
        self.manager.set_slideshow_disabled()

    def _reset_countdown(self):
        interval = int(self.interval_seconds)
        self._next_at = time.monotonic() + interval

        if getattr(self, "_slideshow_after_id", None):
            self.root.after_cancel(self._slideshow_after_id)

        self._slideshow_after_id = self.root.after(interval * 1000, self._slideshow_step)

    def _slideshow_step(self):
        if not self.manager.is_slideshow_enabled():
            self.timer_var.set("Not running")
            return

        if self.manager.images:
            path = self.manager.next_wallpaper()
            if path:
                self.status_var.set(f"Slideshow: {path}")

        self._reset_countdown()

    def _create_tray_icon(self):
        image = Image.new("RGB", (16, 16), "black")

        menu = pystray.Menu(
            Item("Start Slideshow", self.start_slideshow),
            Item("Stop Slideshow", self.stop_slideshow),
            Item("Next Now", self.next_now),
            Item("Show Window", self.show_window),
            Item("Hide Window", self.hide_window),
            Item("Quit", None),
        )

        self.tray_icon = pystray.Icon("wallpaper_changer", image, "Wallpaper Changer", menu)
        self.tray_icon.run_detached()

    def tray_quit(self, icon, menu_item):
        icon.stop()

        def _quit():
            self.manager.set_slideshow_disabled()
            self.root.quit()
            self.root.destroy()

        self.root.after(0, _quit)

    def _start_tray_icon(self):
        self.root.after(0, self._create_tray_icon)

    def _schedule_slideshow_step(self):
        self.manager.set_slideshow_enabled()

        if getattr(self, "_slideshow_after_id", None):
            self.root.after_cancel(self._slideshow_after_id)
        if getattr(self, "_tick_after_id", None):
            self.root.after_cancel(self._tick_after_id)

        interval = int(self.interval_seconds)
        self._next_at = time.monotonic() + interval

        def tick():
            if not self.manager.is_slideshow_enabled():
                self.timer_var.set("Not running")
                return
            remaining = max(0, int(self._next_at - time.monotonic()))
            self.timer_var.set(f"Next in: {remaining} seconds")
            self._tick_after_id = self.root.after(1000, tick)

        tick()
        self._slideshow_after_id = self.root.after(interval * 1000, self._slideshow_step)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root, 10)
    root.mainloop()
