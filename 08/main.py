import os
import datetime

backup_dir = "backup/"

files = os.listdir()

for file in files:
    if not file.endswith(".txt"):
        continue
    file = file.replace(".txt", "")

    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S.%f")
    backup_folder = os.path.join(backup_dir, file)
    os.makedirs(backup_folder, exist_ok=True)

    file_path = os.path.join(backup_folder, f"{current_time[:-3]}.txt")
    print(f"Saving the file as {file_path}")
    with open(file_path, "w") as f:
        with open(f"{file}.txt", "r") as f2:
            content = f2.read()
            f.write(content)
