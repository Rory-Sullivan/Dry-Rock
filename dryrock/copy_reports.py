import pathlib
import shutil


def copy_index():
    """Copies index.html from the output folder into the current directory."""

    src_file = pathlib.Path("./pages/index.html")
    destination = "."

    shutil.copy(src_file, destination)
