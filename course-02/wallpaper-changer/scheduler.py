from typing import Any, Callable, Protocol

Handle = Any


class Scheduler(Protocol):
    def call_later(self, delay_ms: int, cb: Callable[[], None]) -> Handle: ...

    def cancel(self, handle: Handle) -> None: ...


class TkScheduler:

    def __init__(self, root: Any):
        self._root = root

    def call_later(self, delay_ms: int, cb: Callable[[], None]) -> Handle:
        return self._root.after(delay_ms, cb)

    def cancel(self, handle: Handle) -> None:
        try:
            self._root.after_cancel(handle)
        except Exception:
            pass


class ManualScheduler:
    def __init__(self):
        self._next_id = 1
        self._tasks: dict[int, tuple[int, Callable[[], None]]] = {}

    def call_later(self, delay_ms: int, cb: Callable[[], None]) -> Handle:
        hid = self._next_id
        self._next_id += 1
        self._tasks[hid] = (delay_ms, cb)
        return hid

    def cancel(self, handle: Handle) -> None:
        self._tasks.pop(int(handle), None)

    def run_all(self) -> None:
        tasks = list(self._tasks.items())
        self._tasks.clear()
        for _, (_, cb) in tasks:
            cb()
