import os
import itertools
from lib import set_wallpaper
from configurator import Configurator


class WallpaperManager:
    def __init__(self):
        self.configurator = Configurator()
        self.folder = self.configurator.get("selected_folder", "")
        self.images = []
        self.cycle = None
        self._slideshow_enabled = self.configurator.get("is_slideshow_enabled", False)

        self.set_folder(self.folder)
        if self.configurator.get("current_wallpaper"):
            self._set_stored_wallpaper(self.configurator.get("current_wallpaper"))

    def _load_images(self, folder: str):
        if not folder or not os.path.isdir(self.folder):
            return []
        self.configurator.set("selected_folder", folder)
        valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        files = []
        for name in os.listdir(folder):
            if os.path.splitext(name)[1].lower() not in valid_extensions:
                continue
            files.append(os.path.join(folder, name))
        return files

    def _set_stored_wallpaper(self, path: str):
        if path not in self.images:
            self.configurator.delete("current_wallpaper")
            return
        while True:
            current = next(self.cycle)
            if current == path:
                break

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
        self.configurator.set("current_wallpaper", path)
        set_wallpaper(path)
        return path

    def is_slideshow_enabled(self):
        return self._slideshow_enabled

    def set_slideshow_enabled(self):
        self.configurator.set("is_slideshow_enabled", True)
        self._slideshow_enabled = True

    def set_slideshow_disabled(self):
        self.configurator.set("is_slideshow_enabled", False)
        self._slideshow_enabled = False
