import re
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag, ResultSet

from constants import AttrName, BS_PARSER, TagName
from parsers.utils import DateTimeWorker as dtw


class URLParser:
    """
    Сollects download links.

    Args:
        - **url** - base url;
        - **pattern** - pattern for download links;
        - **delta_days** - period in days for which
        files are required.
    """

    def __init__(self, url: str, pattern: str, delta_days: int = 0) -> None:
        self._url = url
        self._delta = dtw.get_timedelta(delta_days)
        self._pattern = self._compile(pattern)
        self.__parser = BS_PARSER
        self._flag = True

    def _compile(self, pattern: str) -> re.Pattern[str]:
        """Returns the compiled pattern."""
        return re.compile(pattern)

    def _contains(self, text: str) -> Optional[re.Match]:
        """
        Returns a match between
        an attribute value and a pattern.
        """
        return self._pattern.search(text)

    def _get_inner_tag(
        self,
        soup: BeautifulSoup,
        outer_tag: str,
        inner_tag: str,
        out_attrs: Optional[dict] = None,
        in_attrs: Optional[dict] = None
    ) -> Optional[Tag]:
        """
        Retruns the inner tag with given the attribute name
        and its value for the outer and the inner tag.
        """
        return soup.find(outer_tag, out_attrs).find(inner_tag, in_attrs)

    def _parse_links_with_date(self, items: ResultSet) -> list[str]:
        """
        Verified the link and the specified time period.
        Returns a list of verified links.
        """
        verified_links: list = []
        current_date = dtw.get_current_date()

        for item in items:
            link: str = item.find(TagName.A).get(AttrName.HREF)

            if not self._contains(link):
                break

            date = dtw.create_date(
                item.find(TagName.P).find(TagName.SPAN).text
            )

            if date <= current_date - self._delta:
                self._flag = False
                break

            link = link.split('?')[0]
            verified_links.append(self._url + link)

        return verified_links

    def parse_upload_links(self, endpoint: str, tag_attrs: dict) -> list[str]:
        """
        Accepts an endpoint and a dict with attributes
        to search download links.
        """
        response = requests.get(self._url + endpoint)
        soup = BeautifulSoup(response.content, self.__parser)
        upload_endpoints: list[str] = []

        while self._flag:
            items: ResultSet = soup.find_all(
                TagName.DIV, tag_attrs.get(TagName.DIV)
            )
            upload_endpoints.extend(
                self._parse_links_with_date(items)
            )

            next_page = self._get_inner_tag(
                soup,
                TagName.LI,
                TagName.A,
                {AttrName.KLASS: tag_attrs.get(TagName.LI)}
            )
            if not next_page:
                break

            next_page = next_page.get(AttrName.HREF)

            response = requests.get(self._url + next_page)
            soup = BeautifulSoup(response.content, self.__parser)

        return upload_endpoints
