import os
import json
import time
import re

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from automation import utils, content, captcha

COOKIES_PATH = "./cookies.json"


def main_rates(chrome=None, auto=False):
    if chrome is None:
        chrome = utils.new_chrome()
        if os.path.exists(COOKIES_PATH):
            utils.load_cookies(chrome, COOKIES_PATH)
        chrome.get("https://main.m.taobao.com/mytaobao/index.html")
        input("登录完毕后按Enter")
        item_id = int(input("Item ID: "))
        chrome.get(content.RATELIST_URL.format(item_id=item_id))
    if auto:
        try:
            while True:
                body = chrome.find_element(By.TAG_NAME, "body")
                # chrome.execute_script("arguments[0].focus();", body)
                body.click()
                body.send_keys(*([Keys.ARROW_DOWN] * 100))
                time.sleep(1)
                if captcha.check_captcha(chrome):
                    captcha.pass_slidecaptcha_pag(chrome)
        except KeyboardInterrupt:
            pass
    else:
        input("手动下拉刷新页面，完成后按 Enter")
    print("saving...")
    rates = content.get_ratelist(chrome)
    if s := re.search(r"auctionNumId=(\d+)", chrome.current_url):
        item_id = int(s.group(1))
    with open(
        f"./{item_id}_{len(rates)}_{int(time.time())}.json", "w+", encoding="utf-8"
    ) as fp:
        json.dump(rates, fp, indent=4, ensure_ascii=False)
    utils.save_cookies(chrome, COOKIES_PATH)
    return chrome


def main_items():
    raise NotImplementedError
    chrome = utils.new_chrome(mobile=False)
    if os.path.exists(COOKIES_PATH):
        utils.load_cookies(chrome, COOKIES_PATH)
    chrome.get("https://www.taobao.com/")
    input("登录完毕后按Enter")


# if __name__ == "__main__":
#     main_rates()
