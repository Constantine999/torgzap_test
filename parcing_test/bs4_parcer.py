from http import HTTPStatus

import requests
from bs4 import BeautifulSoup
from loguru import logger
from requests.exceptions import ConnectionError, HTTPError

from parcing_test import log
from parcing_test.utils import ParcerNews


class BS4ParcerNews(ParcerNews):
    def _parce_last_news(self) -> None:
        for link in list(self.links)[:5]:
            try:
                response = self._get_soup(f"{self.url}{link}")
                news = {
                    "category": response.find("h1").text.strip(),
                    "title": response.find("a", class_="list-item__title color-font-hover-only").text,
                    "link": response.find("a", class_="list-item__title color-font-hover-only").get("href"),
                    "description": "",
                }
            except AttributeError as error:
                logger.error(error := f"{error}, url={self.url + link}")
                raise AttributeError(error)
            else:
                self.news.append(news)

    def _get_links(self) -> None:
        self.links = set()
        response = self._get_soup(self.url).find_all("div", class_="cell-extension__item m-with-title")

        try:
            for obj in response:
                link: str = obj.find("a").get("href")
                if link.startswith("/") and "tourism" not in link:
                    self.links.add(link)
        except AttributeError as error:
            logger.error(error)
            raise AttributeError(error)

    def _get_soup(self, url: str) -> BeautifulSoup:
        """Get soup object."""
        try:
            response = requests.get(url)
            if response.status_code == HTTPStatus.OK:
                return BeautifulSoup(response.text, "html.parser")

        except (HTTPError, ConnectionError) as error:
            logger.error(error)
            raise requests.exceptions.HTTPError(error)


