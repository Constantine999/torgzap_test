import uvicorn
from fastapi import FastAPI, HTTPException, status
from loguru import logger
from pydantic import BaseModel
from requests.exceptions import ConnectionError, HTTPError
from selenium.common import NoSuchElementException

from bs4_parcer import BS4ParcerNews
from selenium_parcer import SeleniumParcerNews
from utils import read_file_csv, write_file_csv

app = FastAPI()


class NewsModel(BaseModel):
    category: str
    title: str
    link: str
    description: str


@app.get("/news_selenium/", tags=["get_news"])
async def get_news_selenium() -> list[NewsModel]:
    try:
        return read_file_csv()
    except FileNotFoundError as error:
        logger.error(f"Error {get_news_selenium.__name__} - {error}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The data file is missing",
        )


@app.get("/selenium_parcer_news/", tags=["selenium_parcer"], status_code=status.HTTP_201_CREATED)
async def use_selenium_parcer_news() -> dict[str, str]:
    try:
        parcer = SeleniumParcerNews()
        write_file_csv(parcer.filename, parcer.news)
        return {"message": "Parsing is done"}
    except (NoSuchElementException, FileNotFoundError) as error:
        logger.error(f"Error in function {use_selenium_parcer_news.__name__} - {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error was detected during parsing",
        )


@app.get("/bs4_parcer_news/", tags=["bs4_parcer"], status_code=status.HTTP_201_CREATED)
async def use_bs4_parcer_news() -> dict[str, str]:
    try:
        parcer = BS4ParcerNews()
        write_file_csv(parcer.filename, parcer.news)
        return {"message": "Parsing is done"}
    except (HTTPError, ConnectionError, AttributeError) as error:
        logger.error(f"Error in function {use_bs4_parcer_news.__name__} - {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error was detected during parsing",
        )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=False, port=5000)
