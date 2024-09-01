import random
import ctypes
import functools

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import InvalidArgumentException


def no_exception(exceptions=(Exception,), rv_when_error=None):
    def decorator(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions:
                return rv_when_error

        return wrapped

    return decorator


def check_result(func):
    @functools.wraps(func)
    def wrapped(chrome: webdriver.Chrome):
        func(chrome)
        try:
            chrome.find_element(By.CLASS_NAME, "errloading").click()
            return False
        except Exception:
            return True

    return wrapped


@no_exception(rv_when_error=False)
def check_captcha(chrome: webdriver.Chrome):
    return bool(
        chrome.find_elements(by=By.CLASS_NAME, value="J_MIDDLEWARE_FRAME_WIDGET")
        or chrome.find_elements(by=By.CLASS_NAME, value="captcha")
    )


def pass_slidecaptcha_wwwwww(chrome: webdriver.Chrome):
    if _ := chrome.find_elements(by=By.CLASS_NAME, value="J_MIDDLEWARE_FRAME_WIDGET"):
        delete_element(chrome, _[0])


@no_exception(exceptions=(InvalidArgumentException,))
@check_result
def pass_slidecaptcha_pag(chrome: webdriver.Chrome):
    if chrome.find_elements(by=By.TAG_NAME, value="iframe"):
        chrome.switch_to.frame(0)
    if not (_ := chrome.find_elements(by=By.CLASS_NAME, value="nc_iconfont")):
        return None
    dragbar = _[0]
    x, y = get_element_center_screen_coordinates(chrome, dragbar)
    outline = chrome.find_element(By.CLASS_NAME, "slidetounlock")
    width = outline.size["width"]

    pyautogui.moveTo(x, y)
    pyautogui.dragRel(
        width + 200 + random.randint(20, 60),
        random.randint(-50, 50),
    )
    chrome.implicitly_wait(3)


@no_exception(exceptions=(InvalidArgumentException,))
@check_result
def pass_slidecaptcha(chrome: webdriver.Chrome):
    if frames := chrome.find_elements(by=By.TAG_NAME, value="iframe"):
        chrome.switch_to.frame(frames[0])
    if not (_ := chrome.find_elements(by=By.CLASS_NAME, value="nc_iconfont")):
        return None
    dragbar = _[0]

    outline = chrome.find_element(By.CLASS_NAME, "slidetounlock")
    width = outline.size["width"]

    chrome.implicitly_wait(3)
    actions = ActionChains(chrome)
    actions.click_and_hold(dragbar)
    actions.pause(1)
    actions.move_by_offset(width + random.randint(0, 50), random.randint(-50, 50))
    actions.pause(1)
    actions.release().perform()

    chrome.implicitly_wait(3)

    if _ := chrome.find_elements(By.CLASS_NAME, "errloading"):
        _[0].click()
        return False
    return True


def delete_element(chrome: webdriver.Chrome, element: WebElement) -> None:
    chrome.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element)


def get_browser_window_adjustments(driver: webdriver.Chrome):
    """
    获取浏览器窗口边框和标题栏的高度和宽度
    """
    window_size = driver.execute_script(
        """
    return {
        'innerWidth': window.innerWidth,
        'innerHeight': window.innerHeight,
        'outerWidth': window.outerWidth,
        'outerHeight': window.outerHeight,
    };"""
    )

    border_width = (window_size["outerWidth"] - window_size["innerWidth"]) / 2
    title_bar_height = (
        window_size["outerHeight"] - window_size["innerHeight"] - border_width
    )

    return border_width, title_bar_height


def get_element_center_screen_coordinates(driver, elem):
    element_location = elem.location
    element_size = elem.size

    element_center_x = element_location["x"] + element_size["width"] / 2
    element_center_y = element_location["y"] + element_size["height"] / 2

    window_position = driver.get_window_position()
    border_width, title_bar_height = get_browser_window_adjustments(driver)

    element_center_absolute_x = window_position["x"] + element_center_x + border_width
    element_center_absolute_y = (
        window_position["y"] + element_center_y + title_bar_height
    )

    scale_factor = get_screen_scale_factor()

    return (
        element_center_absolute_x * scale_factor,
        element_center_absolute_y * scale_factor,
    )


def get_screen_scale_factor():
    user32 = ctypes.windll.user32
    dpi = user32.GetDpiForWindow(user32.GetForegroundWindow())
    scale_factor = dpi / 96  # 96 -> 100%
    return scale_factor
