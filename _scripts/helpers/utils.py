import os
import subprocess


def sleep_cmd(seconds):
    # if system() == "Windows":
    #     run(f"ping 127.0.0.1 -n {seconds} > nul", shell=True)
    # else:
    #     run(f"sleep {seconds}", shell=True)
    subprocess.run(f"sleep {seconds}", shell=True)  # mingw sleep on windows


def get_dir_modified_times(directory):
    modified_times = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("~"):
                continue
            file_path = os.path.join(root, file)
            modified_times[file_path] = os.path.getmtime(file_path)
    return modified_times