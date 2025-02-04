# import os
# import datetime
import os.path
# from datetime import datetime
from datetime import datetime as dt

from os import listdir, makedirs
from os.path import join
import test
import shutil


def is_this_file_correct(file):
    self_path = os.path.abspath(__file__)
    return os.path.abspath(file) != self_path


def is_folder(file):
    return os.path.isdir(file)


backup_dir = "backup/"


def main():
    files = listdir()

    for file in files:
        if not is_this_file_correct(file) or is_folder(file):
            continue

        file, ext = os.path.splitext(file)

        current_time = dt.now().strftime("%Y_%m_%d_%H_%M_%S.%f")
        backup_folder = join(backup_dir, file)
        makedirs(backup_folder, exist_ok=True)

        file_path = join(backup_folder, f"{current_time[:-3]}{ext}")
        print(f"Saving the file as {file_path}")
        shutil.copy(f"{file}{ext}", file_path)


if __name__ == "__main__":
    main()
