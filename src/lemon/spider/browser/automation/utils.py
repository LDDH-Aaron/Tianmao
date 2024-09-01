import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

__all__ = [
    "new_chrome",
    "save_cookies",
    "load_cookies",
]

MOBILE_UA = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"


def new_chrome(
    chromebin="./chrome-win/chrome.exe",
    chromedriverbin="./chrome-win/chromedriver.exe",
    mobile=True,
) -> webdriver.Chrome:
    option = Options()
    option.binary_location = chromebin
    if mobile:
        option.add_argument(f"--user-agent={MOBILE_UA}")
    option.add_experimental_option(
        "excludeSwitches", ["load-extension", "enable-automation"]
    )
    option.add_experimental_option("useAutomationExtension", False)
    option.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(executable_path=chromedriverbin)
    browser = webdriver.Chrome(options=option, service=service)
    browser.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                    }
                )
            """
        },
    )
    return browser


def save_cookies(chrome: webdriver.Chrome, file: str = "./cookies.json"):
    cookies = chrome.get_cookies()
    with open(file, "w+", encoding="utf-8") as fp:
        json.dump(cookies, fp)


def load_cookies(chrome: webdriver.Chrome, file: str = "./cookies.json"):
    with open(file, "r", encoding="utf-8") as fp:
        cookies = json.load(fp)

    cookies_by_domain: dict[str, list[dict]] = {}
    for cookie in cookies:
        domain = cookie["domain"]
        if domain not in cookies_by_domain:
            cookies_by_domain[domain] = []
        cookies_by_domain[domain].append(cookie)

    for domain, domain_cookies in cookies_by_domain.items():
        url = f"http://{domain.lstrip('.')}"
        chrome.get(url)
        for cookie in domain_cookies:
            if isinstance(cookie.get("expiry"), float):
                cookie["expiry"] = int(cookie["expiry"])
            chrome.add_cookie(cookie)
        chrome.refresh()


