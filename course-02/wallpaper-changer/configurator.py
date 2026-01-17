import platform
import os
import json

CONFIG_FILE_NAME = "config.json"


def get_config_path():
    home_folder = os.path.expanduser("~")
    system = platform.system()
    if system == "Windows":
        folder = os.path.join(home_folder, "AppData", "Local", "WallpaperChanger")
    else:
        folder = os.path.join(home_folder, ".config", "WallpaperChanger")

    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def get_config_file_path():
    config_folder = get_config_path()
    config_file = os.path.join(config_folder, CONFIG_FILE_NAME)
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            f.write("{}")
    return config_file


class Configurator:
    def __init__(self):
        self.config_file = get_config_file_path()

    def get(self, key, default=None):
        with open(self.config_file, "r") as f:
            config = json.load(f)
        return config.get(key, default)

    def set(self, key, value):
        with open(self.config_file, "r") as f:
            config = json.load(f)

        config[key] = value
        with open(self.config_file, "w") as f:
            json.dump(config, f)

    def delete(self, key):
        with open(self.config_file, "r") as f:
            config = json.load(f)

        if key in config:
            del config[key]
            with open(self.config_file, "w") as f:
                json.dump(config, f)
