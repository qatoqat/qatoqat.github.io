# module
import filecmp
import os
import shutil


def mirror_file(src_path, dest_path):
    if os.path.exists(dest_path) and filecmp.cmp(src_path, dest_path, shallow=True):
        return
    shutil.copy2(src_path, dest_path)
    print(f"Copied file: {src_path} to {dest_path}")


def mirror_directory(src, dest):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory {src} does not exist.")

    os.makedirs(dest, exist_ok=True)

    src_files = set(os.listdir(src))
    for item in src_files:
        src_path = f"{src}/{item}"
        dest_path = f"{dest}/{item}"

        if os.path.isdir(src_path):
            mirror_directory(src_path, dest_path)
        else:
            mirror_file(src_path, dest_path)

    dest_files = set(os.listdir(dest))
    files_to_remove = dest_files - src_files

    for item in files_to_remove:
        dest_path = f"{dest}/{item}"
        if os.path.isdir(dest_path):
            shutil.rmtree(dest_path)
            print(f"Removed directory: {dest_path}")
        else:
            os.remove(dest_path)
            print(f"Removed file: {dest_path}")
