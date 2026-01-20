from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image
import pystray
from pystray import MenuItem as Item
import platform

if TYPE_CHECKING:
    from application import App


class TrayIcon:
    def __init__(self, app: App, manager):
        self.app = app
        self.manager = manager
        self.tray_icon = None

    def _wrap(self, fn):
        def _cb(icon, item):
            self.app.root.after(0, fn)

        return _cb

    def _create_tray_icon(self):
        image = Image.open("icon.png")

        menu = pystray.Menu(
            Item("Start Slideshow", self._wrap(self.app.start_slideshow)),
            Item("Stop Slideshow", self._wrap(self.app.stop_slideshow)),
            Item("Next Now", self._wrap(self.app.next_now)),
            Item("Show Window", self._wrap(self.app.show_window)),
            Item("Hide Window", self._wrap(self.app.hide_window)),
            Item("Quit", self.tray_quit),
        )

        self.tray_icon = pystray.Icon("wallpaper_changer", image, "Wallpaper Changer", menu)
        self.tray_icon.run_detached()

    def tray_quit(self, icon, menu_item):
        icon.stop()

        def _quit():
            self.manager.stop_slideshow()
            self.app.root.quit()
            self.app.root.destroy()

        self.app.root.after(0, _quit)

    def start(self):
        if platform.system() == "Darwin":
            return
        self.app.root.after(0, self._create_tray_icon)
