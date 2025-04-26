import http.server
import mimetypes
import os
import socketserver
import time
from threading import Thread

from helpers.mirror import mirror_directory
from helpers.utils import sleep_cmd, get_dir_modified_times

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
hot_reload_script = """
<script>
console.log("Hot reload is enabled");

let reloadInterval;
let wasPaused = false;

function startPolling() {
    reloadInterval = setInterval(() => {
        fetch("/__ping__")
            .then(res => res.text())
            .then(ts => {
                if (window.__last_reload_ts && window.__last_reload_ts !== ts) {
                    location.reload();
                }
                window.__last_reload_ts = ts;
            })
            .catch(() => {
            });
    }, 1000);
}

function stopPolling() {
    if (reloadInterval) {
        clearInterval(reloadInterval);
        reloadInterval = null;
    }
}

document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        if (!reloadInterval) {
            startPolling();
            if (wasPaused) {
                console.log("Hot reload is resumed");
            }
        }
    } else {
        stopPolling();
        wasPaused = true;
        console.log("Hot reload is paused");
    }
});

if (document.visibilityState === 'visible') {
    startPolling();
}
</script>
"""


def mirror_server_files():
    for key, value in SRC_DEST_DIRS.items():
        if key != value:
            mirror_directory(key, value)


def get_modified_times():
    modified_times = {}
    for key in SRC_DEST_DIRS.keys():
        modified_times.update(get_dir_modified_times(key))
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
