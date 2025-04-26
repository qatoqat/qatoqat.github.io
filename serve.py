import filecmp
import http.server
import mimetypes
import os
import shutil
import socketserver
import time
from subprocess import run
from threading import Thread

# -- config --
DEST_ROOT_DIR = "public"

SRC_DEST_DIRS = {
    DEST_ROOT_DIR: DEST_ROOT_DIR,
    "assets": DEST_ROOT_DIR + "/assets",
    "partials": DEST_ROOT_DIR + "/partials",
}

ADDRESS = "127.0.0.1"
PORT = 8000

last_modified = str(time.time())
server_ref: socketserver.TCPServer | None = None

# -- utils --
hot_reload_script = "<script src='/hot-reload.js'></script>"


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


def sleep_cmd(seconds):
    # if system() == "Windows":
    #     run(f"ping 127.0.0.1 -n {seconds} > nul", shell=True)
    # else:
    #     run(f"sleep {seconds}", shell=True)
    run(f"sleep {seconds}", shell=True)  # mingw sleep on windows


def get_last_modified_times(directory):
    modified_times = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            modified_times[file_path] = os.path.getmtime(file_path)
    return modified_times


def mirror_server_files():
    for key, value in SRC_DEST_DIRS.items():
        mirror_directory(key, value)


def get_modified_times():
    modified_times = {}
    for key in SRC_DEST_DIRS.keys():
        modified_times.update(get_last_modified_times(key))
    return modified_times


def start_server_with_hot_reload():
    mirror_server_files()
    last_modified_times = get_modified_times()

    update_timestamp()
    print("Hot reload is enabled")

    start_server_thread()

    while True:
        if server_ref is None:
            print("Server thread has not started yet. Waiting for 5 seconds ...")
            sleep_cmd(5)
            continue
        current_modified_times = get_modified_times()

        if last_modified_times != current_modified_times:
            last_modified_times = current_modified_times
            print("Files have changed, restarting server ...")
            stop_server()
            # if WEB_SRC_DIR != WEB_DEST_DIR:
            #     mirror_server_files()
            mirror_server_files()
            start_server_thread()
            update_timestamp()
        sleep_cmd(1)


def update_timestamp():
    global last_modified
    last_modified = str(time.time())


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DEST_ROOT_DIR, **kwargs)

    def do_GET(self):
        if self.path == "/__ping__":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            global last_modified
            self.wfile.write(last_modified.encode())
        else:
            super().do_GET()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            for index in ("index.html", "index.htm"):
                index_path = os.path.join(path, index)
                if os.path.exists(index_path):
                    path = index_path
                    break

        if os.path.isfile(path):
            mime_type, _ = mimetypes.guess_type(path)
            if mime_type == "text/html":
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if "</body>" in content:
                    content = content.replace("</body>", f"</body>{hot_reload_script}")
                else:
                    content += hot_reload_script

                encoded = content.encode('utf-8')
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)
                return None

        return super().send_head()

    # noinspection PyShadowingBuiltins
    def log_message(self, format, *args):
        if self.path == "/__ping__":
            return

        super().log_message(format, *args)


def start_server():
    with socketserver.TCPServer((ADDRESS, PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving at http://{ADDRESS}:{PORT}")
        global server_ref
        server_ref = httpd
        httpd.serve_forever()


def start_server_thread():
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()


def stop_server():
    global server_ref
    if server_ref:
        server_ref.shutdown()


if __name__ == '__main__':
    start_server_with_hot_reload()
