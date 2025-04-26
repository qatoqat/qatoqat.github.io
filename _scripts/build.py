from helpers.mirror import mirror_directory
from helpers.page import generate_html_files

generate_html_files()

DEST_ROOT_DIR = "public"

SRC_DEST_DIRS = {
    DEST_ROOT_DIR: DEST_ROOT_DIR,
    "assets": DEST_ROOT_DIR + "/assets",
    "partials": DEST_ROOT_DIR + "/partials",
}

for key, value in SRC_DEST_DIRS.items():
    if key != value:
        mirror_directory(key, value)
