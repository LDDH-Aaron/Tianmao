from typing import TypedDict, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

# from .captcha import check_captcha

RATELIST_URL = (
    "https://h5.m.taobao.com/app/rate/www/rate-list/index.html?auctionNumId={item_id}"
)
INFO_URL = "https://h5.m.taobao.com/awp/core/detail.htm?id={item_id}"

TITLE_XPATH = '//*[@id="titleSection"]/div/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/div[5]/div/span[1]'


class Rate(TypedDict):
    username: str
    date: str
    sku: str
    title: str
    content: str


class Item(TypedDict):
    title: str


def get_info(chrome: webdriver.Chrome, item_id: int):
    chrome.get(INFO_URL.format(item_id=item_id))
    # title = chrome.find_element(By.XPATH, TITLE_XPATH).text
    return NotImplemented


def get_ratelist(chrome: webdriver.Chrome):
    assert (
        "h5.m.taobao.com/app/rate/www/rate-list/index.html" in chrome.current_url
    ), "wrong page"
    container = chrome.find_element(By.CLASS_NAME, "rax-scrollview-webcontainer")
    return [
        extract_rate(rate)
        for rate in container.find_elements(By.CLASS_NAME, "card__main")
    ]


def find_noexcept(elem: WebElement, by: By, value: Any):
    try:
        return elem.find_element(by, value).text
    except NoSuchElementException:
        return ""


def extract_rate(rate_elem: WebElement):
    date, sku = find_noexcept(rate_elem, by=By.CLASS_NAME, value="card__sku").split(
        maxsplit=1
    )
    return Rate(
        username=find_noexcept(rate_elem, by=By.CLASS_NAME, value="user__name"),
        date=date,
        sku=sku,
        title=find_noexcept(rate_elem, by=By.CLASS_NAME, value="card__title"),
        content=find_noexcept(rate_elem, by=By.CLASS_NAME, value="card__content"),
    )
