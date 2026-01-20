import platform
import tkinter as tk
from tkinter import filedialog, messagebox

from manager import WallpaperManager
from scheduler import TkScheduler
from lib import set_wallpaper
from api import API
from tray import TrayIcon


class App:
    def __init__(self, _root: tk.Tk, interval_seconds: int):
        self.root = _root
        self._setup_root()

        self.scheduler = TkScheduler(self.root)
        self.manager = WallpaperManager(self.scheduler)
        self.api = API()

        self.folder_var = tk.StringVar(None, self.manager.folder)
        self.status_var = tk.StringVar()
        self.timer_var = tk.StringVar()
        self.interval_seconds = interval_seconds

        self.tray_icon = TrayIcon(self, self.manager)

        self.manager.attach_ui_hooks(
            on_status=self.status_var.set,
            on_timer=self.timer_var.set,
        )

        self._build_ui()
        self.tray_icon.start()


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

    def _setup_root(self):
        self.root.title("Wallpaper Changer")
        self.root.resizable(False, False)

        if platform.system() == "Windows":
            self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
            self.root.withdraw()
            self.root.attributes("-toolwindow", True)

        try:
            icon = tk.PhotoImage(file="icon.png")
            self.root.iconphoto(True, icon)
        except Exception as e:
            print("Could not load app icon:", e)

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

        api_btn = tk.Button(btn_frame, text="Get API wallpaper", command=self.api_wallpaper)
        api_btn.pack(side="left", padx=5)

        status_frame = tk.Frame(self.root)
        status_frame.pack(padx=10, pady=(0, 5), fill="x")

        timer_lbl = tk.Label(status_frame, textvariable=self.timer_var)
        timer_lbl.pack(side="left")

        status_lbl = tk.Label(status_frame, textvariable=self.status_var)
        status_lbl.pack(side="right")

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

        self.manager.reset_countdown()

    def next_now(self):
        if not self.manager.images:
            messagebox.showwarning("no images", "please select a folder with images first.")
            return

        path = self.manager.next_wallpaper()
        if path:
            self.status_var.set(f"Set wallpaper: {path}")

        self.manager.reset_countdown()

    def api_wallpaper(self):
        path = self.api.get_wallpaper()
        if path:
            set_wallpaper(path)
            self.status_var.set(f"API wallpaper: {path}")

    def start_slideshow(self):
        if not self.manager.images:
            messagebox.showwarning("no images", "please select a folder with images first.")
            return

        self.manager.start_slideshow(int(self.interval_seconds))

    def stop_slideshow(self):
        self.manager.stop_slideshow()

