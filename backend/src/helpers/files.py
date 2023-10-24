import os
from pathlib import Path
from typing import Optional, Union

from core.constants import DOWNLOAD_DIR


class PlatformFileWorker:
    """Helper class for working with files on the platform."""

    @classmethod
    def handle_path(
        cls,
        path: Optional[Union[Path, str]]
    ) -> Path:
        """Path handler. Creates default dir if path is None."""
        if not path:
            default_path: Path = DOWNLOAD_DIR
            cls.__make_dir_if_not_exist(default_path)
            return default_path

        path: Path = Path(path)
        cls.__make_dir_if_not_exist(path)
        return path

    @classmethod
    def __make_dir_if_not_exist(cls, path: Path) -> None:
        """Creates a dir if it doesn't exist."""
        if not path.is_dir():
            path.mkdir()

    @staticmethod
    def get_files(path: Union[Path, str]) -> list[str]:
        """Collects files from the specified dir."""
        files: list[str] = []
        for _, _, file in os.walk(path):
            files.extend(file)

        return files

    @staticmethod
    def remove_file(path: Union[Path, str]) -> None:
        """Remove file from path."""
        if not isinstance(path, Path):
            path = Path(path)

        path.unlink()
