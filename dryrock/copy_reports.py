import pathlib
import shutil

from .config import OUTPUT_PATH


def copy_index():
    """Copies index.html from the output folder into the current directory."""

    src_file = pathlib.Path(OUTPUT_PATH).joinpath("webpages/index.html")
    destination = "."

    shutil.copy(src_file, destination)
