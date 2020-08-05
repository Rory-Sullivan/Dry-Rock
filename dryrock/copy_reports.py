import pathlib
import shutil

from .config import OUTPUT_PATH


def copy_index():
    src_file = pathlib.Path(OUTPUT_PATH).joinpath("webpages/index.html")
    destination = "."

    shutil.copy(src_file, destination)
