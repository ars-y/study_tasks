import asyncio
import os
from http import HTTPStatus
from pathlib import Path
from typing import Optional, Union

import aiohttp
import aiofile
import requests

from constants import DATA_FILES_DIR, DOWNLOAD_DIR


class FileDownloader:
    """
    Base file donwloader.

    Args:
        - **urls** - list of urls for downloading files;
        - **dir_path** - directory for download files.
    """

    def __init__(
        self,
        urls: list[str],
        dir_path: Optional[Union[Path, str]] = None
    ) -> None:
        self._urls = urls
        self._path = self.__handle_dir_path(dir_path)

    def __handle_dir_path(
        self,
        path: Optional[Union[Path, str]]
    ) -> Path:
        """Path handler. Creates default dir if path is None."""
        if not path:
            for path in (DATA_FILES_DIR, DOWNLOAD_DIR):
                self.__make_dir_if_not_exist(path)
            return DATA_FILES_DIR / DOWNLOAD_DIR

        path: Path = Path(path)
        self.__make_dir_if_not_exist(path)
        return path

    def __make_dir_if_not_exist(self, dir_path: Path) -> None:
        """Creates a dir if it doesn't exist."""
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)


class AsyncFileDownloader(FileDownloader):
    """Asynchronous file downloader."""

    def __init__(
        self,
        urls: list[str],
        dir_path: Optional[Union[Path, str]] = None
    ) -> None:
        super().__init__(urls, dir_path)

        self._semaphore = asyncio.BoundedSemaphore(5)

    async def _fetch(self, session: aiohttp.ClientSession, url: str):
        """Recieves data and writes it to a file."""
        filename: str = url.split('/')[-1]
        path: Path = self._path / filename

        async with self._semaphore:
            async with session.get(url) as response:
                if response.status == HTTPStatus.OK:
                    data = await response.read()

        async with aiofile.async_open(path, 'wb') as file:
            await file.write(data)

    async def _run(self):
        """Gather a list of tasks and execute with session."""
        async with aiohttp.ClientSession() as session:
            tasks: list = [self._fetch(session, url) for url in self._urls]
            await asyncio.gather(*tasks)

    def download(self):
        """Using an event loop to download files async."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run())
        loop.close()


class SyncFileDownloader(FileDownloader):
    """Synchronous file downloader."""

    def _fetch(self, url: str) -> None:
        """Recieves data and writes it to a file."""
        filename: str = url.split('/')[-1]
        path: Path = self._path / filename

        with requests.Session() as session:
            session.trust_env = True

            response = session.get(url)
            if response.status_code == HTTPStatus.OK:
                with open(path, 'wb') as file:
                    file.write(response.content)

    def download(self):
        """In for loop starts downloading a files from the urls list."""
        [self._fetch(url) for url in self._urls]
