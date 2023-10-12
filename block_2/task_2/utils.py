import os
from pathlib import Path
from typing import Union


def get_files(path: Union[Path, str]) -> list[str]:
    """Collects files from the specified dir."""
    files: list[str] = []
    for _, _, file in os.walk(path):
        files.extend(file)

    return files
