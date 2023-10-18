from pathlib import Path

import constants as const
from parsers.datafile import DataFileParser
from parsers.collectors import URLParser
from parsers.loaders import AsyncFileDownloader
from utils import get_files


def main():
    parser = URLParser(const.BASE_URL, const.LINK_PATTERN, const.PERIOD_DAYS)
    links = parser.parse_upload_links(
        const.TRADES_ENDPOINT,
        {
            const.TagName.DIV: const.DIV_TAG_CLASS,
            const.TagName.A: const.A_TAG_CLASS,
            const.TagName.LI: const.LI_TAG_CLASS,
        }
    )
    downloader = AsyncFileDownloader(links)
    downloader.download()
    path: Path = const.DOWNLOAD_DIR
    files: list[str] = get_files(path)

    for file in files:
        parser = DataFileParser(path / file)
        parser.parse()


if __name__ == '__main__':
    main()
