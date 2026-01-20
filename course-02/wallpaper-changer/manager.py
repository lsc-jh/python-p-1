from __future__ import annotations

import os
import itertools
import time
from dataclasses import dataclass
from typing import Callable, Optional, Any

from lib import set_wallpaper
from configurator import Configurator
from scheduler import Scheduler

Handle = Any


@dataclass
class _TimerHandles:
    slideshow: Optional[Handle] = None
    tick: Optional[Handle] = None


class WallpaperManager:
    def __init__(self, scheduler: Scheduler):
        self._scheduler = scheduler

        self.configurator = Configurator()
        self.folder = self.configurator.get("selected_folder", "")
        self.images: list[str] = []
        self.cycle: Optional[itertools.cycle[str]] = None
        self._slideshow_enabled = self.configurator.get("is_slideshow_enabled", False)

        self._handles = _TimerHandles()

        self._interval_seconds: int = 0
        self._next_at: float = 0.0

        self._on_status: Optional[Callable[[str], None]] = None
        self._on_timer: Optional[Callable[[str], None]] = None

        self.set_folder(self.folder)

        stored = self.configurator.get("current_wallpaper")
        if stored:
            self._set_stored_wallpaper(stored)

    def attach_ui_hooks(
            self,
            on_status: Optional[Callable[[str], None]] = None,
            on_timer: Optional[Callable[[str], None]] = None,
    ):
        self._on_status = on_status
        self._on_timer = on_timer

    def _load_images(self, folder: str) -> list[str]:
        if not folder or not os.path.isdir(folder):
            return []
        self.configurator.set("selected_folder", folder)

        valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
        files: list[str] = []
        for name in os.listdir(folder):
            if os.path.splitext(name)[1].lower() not in valid_extensions:
                continue
            files.append(os.path.join(folder, name))
        return files

    def _set_stored_wallpaper(self, path: str):
        if path not in self.images or not self.cycle:
            self.configurator.delete("current_wallpaper")
            return
        while True:
            current = next(self.cycle)
            if current == path:
                break

    def set_folder(self, folder: str):
        self.folder = folder
        self.images = self._load_images(folder)
        self.cycle = itertools.cycle(self.images) if self.images else None

    def next_wallpaper(self) -> Optional[str]:
        if not self.cycle:
            return None
        path = next(self.cycle)
        self.configurator.set("current_wallpaper", path)
        set_wallpaper(path)
        return path

    def is_slideshow_enabled(self) -> bool:
        return self._slideshow_enabled

    def set_slideshow_enabled(self):
        self.configurator.set("is_slideshow_enabled", True)
        self._slideshow_enabled = True

    def set_slideshow_disabled(self):
        self.configurator.set("is_slideshow_enabled", False)
        self._slideshow_enabled = False

    def start_slideshow(self, interval_seconds: int):
        if not self.images:
            self._emit_status("No images loaded.")
            return

        self._interval_seconds = max(1, int(interval_seconds))
        self.set_slideshow_enabled()
        self._emit_status("Slideshow started.")
        self._reset_countdown_and_reschedule()

    def stop_slideshow(self):
        self.set_slideshow_disabled()
        self._cancel_timers()
        self._emit_timer("Not running")
        self._emit_status("Slideshow stopped.")

    def reset_countdown(self):
        if not self.is_slideshow_enabled():
            return
        self._reset_countdown_and_reschedule()

    def _cancel_timers(self):
        if self._handles.slideshow is not None:
            self._scheduler.cancel(self._handles.slideshow)
            self._handles.slideshow = None

        if self._handles.tick is not None:
            self._scheduler.cancel(self._handles.tick)
            self._handles.tick = None

    def _reset_countdown_and_reschedule(self):
        self._cancel_timers()
        self._next_at = time.monotonic() + self._interval_seconds

        def tick():
            if not self.is_slideshow_enabled():
                self._emit_timer("Not running")
                return

            remaining = max(0, int(self._next_at - time.monotonic()))
            self._emit_timer(f"Next in: {remaining} seconds")
            self._handles.tick = self._scheduler.call_later(1000, tick)

        def step():
            if not self.is_slideshow_enabled():
                self._emit_timer("Not running")
                return

            if self.images:
                path = self.next_wallpaper()
                if path:
                    self._emit_status(f"Slideshow: {path}")

            self._reset_countdown_and_reschedule()

        tick()
        self._handles.slideshow = self._scheduler.call_later(self._interval_seconds * 1000, step)

    def _emit_status(self, msg: str):
        if self._on_status:
            self._on_status(msg)

    def _emit_timer(self, msg: str):
        if self._on_timer:
            self._on_timer(msg)
