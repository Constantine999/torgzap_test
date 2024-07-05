from abc import ABC, abstractmethod
from collections import deque
from typing import NewType

import pandas as pd
from loguru import logger

News = NewType("News", dict[str, str])


class ParcerNews(ABC):
    """Abstract class for parce site ria.ru."""

    def __init__(self, filename: str = "news_selenium.csv") -> None:
        self.news = deque(maxlen=5)
        self.url = "https://ria.ru/"
        self.filename = filename
        self._get_links()
        self._parce_last_news()

    @abstractmethod
    def _parce_last_news(self) -> None:
        """Get information about news."""

    @abstractmethod
    def _get_links(self) -> None:
        """Get links categories."""


def read_file_csv(filename: str = "news_selenium.csv") -> list[News]:
    """Read *.csv file."""
    try:
        data = pd.read_csv(filepath_or_buffer=filename).fillna("").to_dict("list")
        return [dict(zip(data.keys(), values)) for values in zip(*data.values())]

    except ValueError as error:
        logger.error(error := f"{error} - file reading error - {filename=}")
        raise ValueError(error)


def write_file_csv(filename: str, data: list[News]) -> None:
    """Write *.csv file."""
    try:
        df = pd.DataFrame(data)
        df.to_csv(path_or_buf=filename, index=False)

    except FileNotFoundError as error:
        logger.error(error := f"{error},{filename=}")
        raise FileNotFoundError(error)
