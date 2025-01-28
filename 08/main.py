# import os
# import datetime

# from datetime import datetime
from datetime import datetime as dt

from os import listdir, makedirs
from os.path import join

backup_dir = "backup/"

files = listdir()

for file in files:
    if not file.endswith(".txt"):
        continue
    file = file.replace(".txt", "")

    current_time = dt.now().strftime("%Y_%m_%d_%H_%M_%S.%f")
    backup_folder = join(backup_dir, file)
    makedirs(backup_folder, exist_ok=True)

    file_path = join(backup_folder, f"{current_time[:-3]}.txt")
    print(f"Saving the file as {file_path}")
    with open(file_path, "w") as f:
        with open(f"{file}.txt", "r") as f2:
            content = f2.read()
            f.write(content)
