from pathlib import Path

import pandas as pd

from core import constants as const
from utils import logger
from db.sessions import LocalSession
from helpers.files import PlatformFileWorker as pfw
from parsers.data import DataXLSParser
from parsers.files import AsyncFileDownloader
from parsers.urls import URLParser
from services.spimex import SpimexService


async def save_data(df: pd.DataFrame) -> None:
    """Saving DataFrame in to SpimexTradingResults table."""
    async with LocalSession() as session:
        await SpimexService.save_trade_dataframe(session, df)


def parse_links() -> list[str]:
    """Returns links for downloading files."""
    parser = URLParser(const.BASE_URL, const.LINK_PATTERN, const.PERIOD_DAYS)
    return parser.parse_upload_links(
        const.TRADES_ENDPOINT,
        {
            const.TagName.DIV: const.DIV_TAG_CLASS,
            const.TagName.A: const.A_TAG_CLASS,
            const.TagName.LI: const.LI_TAG_CLASS,
        }
    )


async def download_files(links: list[str]) -> None:
    """Async download files from a list of links."""
    await AsyncFileDownloader(links).download()


async def run() -> None:
    """Parsing data from downloaded files and save it to a database."""
    logger.info(
        f'Started parsing data from {const.BASE_URL + const.TRADES_ENDPOINT}.'
    )

    await download_files(parse_links())

    path: Path = const.DOWNLOAD_DIR
    files: list[str] = pfw.get_files(path)

    for filename in files:
        path_file = path / filename
        parser = DataXLSParser(path_file)
        await save_data(parser.parse())
        pfw.remove_file(path_file)

    logger.info('Finished parsing data.')
