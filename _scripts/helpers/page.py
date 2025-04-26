import ast
import dataclasses
import os
from pathlib import Path


@dataclasses.dataclass
class Page:
    base = str
    destination = str
    title = str
    scripts = str
    content = str


def get_page_dataclass(file_path: str) -> Page:
    page = Page()
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.Assign):
                target = node.targets[0]
                if isinstance(target, ast.Name):
                    match target.id:
                        case "base":
                            page.base = ast.literal_eval(node.value)
                        case "destination":
                            page.destination = ast.literal_eval(node.value)
                        case "title":
                            page.title = ast.literal_eval(node.value)
                        case "scripts":
                            page.scripts = ast.literal_eval(node.value)
                        case "content":
                            page.content = ast.literal_eval(node.value)
    return page


def get_var_value(file_path: str, var_name: str):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                target = node.targets[0]
                if isinstance(target, ast.Name) and target.id == var_name:
                    return ast.literal_eval(node.value)
    return None


def get_last_modified_times(directory):
    modified_times = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file: str
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                modified_times[file_path] = {
                    "modified_time": os.path.getmtime(file_path),
                    "destination": get_var_value(file_path, "destination")
                }
    return modified_times


def saved_lock_dict(lock_file_str):
    if not lock_file_str.strip():
        return {}
    try:
        saved_lock = ast.literal_eval(lock_file_str)
        if not isinstance(saved_lock, dict):
            return {}
        return saved_lock
    except SyntaxError:
        return {}


def generate_html_files():
    with open("pages.lock", "w+") as lock_file:
        lock_file_str = lock_file.read()
        saved_lock = saved_lock_dict(lock_file_str)
        new_lock = get_last_modified_times("pages")
        new = []
        removed = []
        for key in new_lock:
            if not key in saved_lock or new_lock[key] != saved_lock[key]:
                new.append(key)

        for key in saved_lock:
            if not key in new_lock:
                removed.append(saved_lock[key]["destination"])

        if len(new) == 0 and len(removed) == 0:
            print("No new changes")
        else:
            for f in removed:
                os.remove(f)

            for f in new:
                page = get_page_dataclass(f)
                generate_html(page.base, page.title, page.content, page.scripts, page.destination)
            # update lock
            lock_file.seek(0)
            lock_file.write(str(new_lock))
            lock_file.truncate()


def generate_html(base, title, content, scripts, destination):
    with open(base) as base_file:
        dest_path = Path(destination)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "w") as f:
            f.write(
                base_file.read()
                .replace("{{ title }}", title + " - " if title else "", 1)
                .replace("{{ content }}", content, 1)
                .replace(
                    "{{ scripts }}",
                    "".join([f'<script src="{src}"></script>' for src in scripts]) if scripts else ""
                )
            )
