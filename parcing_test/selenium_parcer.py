from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from parcing_test import log
from parcing_test.utils import ParcerNews


class SeleniumParcerNews(ParcerNews):
    def __init__(self):
        self.__options_chrome = webdriver.ChromeOptions()
        self.__options_chrome.add_argument("--headless")
        super().__init__()

    def _parce_last_news(self) -> None:
        with webdriver.Chrome(
                # options=self.__options_chrome
        ) as driver:
            for link in list(self.links)[:5]:
                try:
                    driver.get(link)
                    news = {
                        "category": driver.find_element(By.TAG_NAME, "h1").text,
                        "title": driver.find_element(By.CSS_SELECTOR, "[class='list-item__title color-font-hover-only']").text,
                        "link": driver.find_element(By.CSS_SELECTOR, "[class='list-item__title color-font-hover-only']").get_attribute("href"),
                        "description": "",
                    }
                except NoSuchElementException as error:
                    logger.error(error := f"{error.msg}, {link=}")
                    raise NoSuchElementException(error)
                else:
                    self.news.append(news)

    def _get_links(self) -> None:
        self.links = set()

        with webdriver.Chrome(
                # options=self.__options_chrome
        ) as driver:
            driver.get(self.url)

            try:
                response = driver.find_elements(By.XPATH, "//div[@class='cell-extension__item m-with-title']")
                for obj in response:
                    link: str = obj.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if link.startswith(self.url) and "tourism" not in link:
                        self.links.add(link)
            except NoSuchElementException as error:
                logger.error(error := f"{error.msg}")
                raise NoSuchElementException(error)
