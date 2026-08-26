from __future__ import annotations

import sys
from collections.abc import Callable

from pynput import keyboard


class GlobalHotkeyListener:
    def __init__(self, hotkey: str, callback: Callable[[], None]) -> None:
        self._hotkey = hotkey
        self._callback = callback
        self._listener: keyboard.GlobalHotKeys | None = None

    def start(self) -> None:
        if sys.platform == "darwin":
            # pynput's macOS listener asks HIToolbox for the current input source
            # (TSMGetInputSourceProperty) from its own thread. macOS 26 asserts that
            # call must be on the main queue and raises SIGTRAP when it is not, so
            # the process dies a few seconds after start — before any Python
            # exception handler can see it.
            # Until this is reimplemented with a main-thread NSEvent monitor, the
            # widget is clicked rather than triggered by a global shortcut.
            return
        self._listener = keyboard.GlobalHotKeys({self._hotkey: self._callback})
        self._listener.start()

    def stop(self) -> None:
        if self._listener is not None:
            self._listener.stop()
