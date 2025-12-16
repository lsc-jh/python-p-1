import os
import itertools
from lib import set_wallpaper


class WallpaperManager:
    def __init__(self):
        self.folder = ""
        self.images = []
        self.cycle = None
        self._slideshow_enabled = False

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

    def is_slideshow_enabled(self):
        return self._slideshow_enabled

    def disable_slideshow(self):
        self._slideshow_enabled = False

    def enable_slideshow(self):
        self._slideshow_enabled = True
