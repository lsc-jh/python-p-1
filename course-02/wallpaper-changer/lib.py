import os
import platform
import subprocess  # macOS only
import ctypes


def set_wallpaper(path: str):
    abs_path = os.path.abspath(path)
    system = platform.system()
    if system == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
    elif system == "Darwin":  # macOS
        script = f'''
        tell application "Finder"
            set desktop picture to POSIX file "{abs_path}"
        end tell
        '''
        subprocess.run(["osascript", "-e", script], check=True)
    else:
        raise NotImplementedError("Setting wallpaper is not implemented for this OS.")
