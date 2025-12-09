import os
import platform
import subprocess
import ctypes

SPI_SETDESKWALLPAPER = 20


def set_wallpaper(path: str):
    path = os.path.abspath(path)
    system = platform.system()

    if system == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, path, 3
        )

    elif system == "Darwin":  # macOS
        script = f'''
        tell application "Finder"
            set desktop picture to POSIX file "{path}"
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")
