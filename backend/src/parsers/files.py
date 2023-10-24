import asyncio
from http import HTTPStatus
from pathlib import Path
from typing import Optional, Union

import aiohttp
import aiofile
import requests

from helpers.files import PlatformFileWorker as pfw


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
        self._path = pfw.handle_path(dir_path)

    def _fetch(self) -> None:
        """Recieves data and writes it to a file."""
        raise NotImplementedError

    def download(self) -> None:
        """Downloads files in a loop and saves them to the system."""
        raise NotImplementedError


class AsyncFileDownloader(FileDownloader):
    """Asynchronous file downloader."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._semaphore = asyncio.BoundedSemaphore(5)

    async def _fetch(self, session: aiohttp.ClientSession, url: str) -> None:
        filename: str = url.split('/')[-1]
        path: Path = self._path / filename

        async with self._semaphore:
            async with session.get(url) as response:
                if response.status == HTTPStatus.OK:
                    data = await response.read()

        async with aiofile.async_open(path, 'wb') as file:
            await file.write(data)

    async def download(self) -> None:
        async with aiohttp.ClientSession() as session:
            tasks: list = [self._fetch(session, url) for url in self._urls]
            await asyncio.gather(*tasks)


class SyncFileDownloader(FileDownloader):
    """Synchronous file downloader."""

    def _fetch(self, url: str) -> None:
        filename: str = url.split('/')[-1]
        path: Path = self._path / filename

        with requests.Session() as session:
            session.trust_env = True

            response = session.get(url)
            if response.status_code == HTTPStatus.OK:
                with open(path, 'wb') as file:
                    file.write(response.content)

    def download(self) -> None:
        [self._fetch(url) for url in self._urls]
