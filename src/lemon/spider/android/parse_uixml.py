import re
from datetime import datetime
from queue import Queue
import time

from lxml import etree
import uiautomator2 as u2
import requests


DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
}


def get_redirect_url(short_url):
    try:
        response = requests.get(
            short_url,
            allow_redirects=True,
            headers=DEFAULT_HEADERS,
            timeout=10,
        )
        return response.url
    except Exception:
        return None


# Rating page
_regex_date = re.compile(r"(\d{4}年)?\d{1,2}月\d{1,2}日")
_regex_detailed_rating = re.compile(r"昵称(.+?)评论(.+?)")
_regex_desc_templ = re.compile(r"(^|\s+)[\u4e00-\u9fa5]{4}：")
# Info page
_regex_title = re.compile(r"alicdn\.com/.+?\.(?=png|jpe?g|gif|webp|avif)")
# Utils
_regex_shortlink = re.compile(r"https://m.tb.cn/[^ \n]+?")
_regex_id_in_url = re.compile(r"[^A-Za-z]id=([0-9]+)")


def get_item_id(s: str):
    if match := _regex_shortlink.search(s):
        if url := get_redirect_url(match.group(0)):
            s = url
    if match := _regex_id_in_url.search(s):
        return int(match.group(1))
    return None


def rm_desc_templ(rate_content: str):
    return _regex_desc_templ.sub(
        " ",
        rate_content.removeprefix("商品评价:")
        .removeprefix("评价标题:")
        .replace("此用户没有填写文本", ""),
    ).strip()


def parse_infopage(device: u2.Device):
    xml = etree.XML(device.dump_hierarchy().encode("utf-8"), etree.XMLParser())
    data = {"title": ""}
    for elem in xml.findall(".//node"):
        if _regex_title.search((line := elem.attrib.get("text", ""))):
            data["title"] = line.split(maxsplit=1)[-1]
            break
    device.xpath("ꈝ").click()
    device.xpath("复制链接").click()
    time.sleep(1)
    data["id"] = get_item_id(device.clipboard)
    return data


def parse_ratingpage(xmlb: bytes, stored: dict[str, str] | None) -> dict[str, str]:
    """
    返回的字典，键为评价内容，值为日期

    stored 参数是已经记录的内容，用于去重
    """
    xml = etree.XML(xmlb, etree.XMLParser())
    nodes: list[str] = [
        e.attrib.get("content-desc", "") for e in xml.findall(".//node")
    ]

    if stored is None:
        stored = {}
    result = {}
    date_to_match: Queue[str] = Queue()
    content_to_match: Queue[str] = Queue()
    for i, node in enumerate(nodes):
        if _regex_date.match(node) and i + 1 < len(nodes):
            date = node
            if "年" not in date:
                date = f"{datetime.now().year}年" + date

            content = rm_desc_templ(nodes[i + 1])
            if content and content not in result and content not in stored:
                result[content] = date
                continue
            # date_to_match.put(date)
            # continue

        # if _regex_detailed_rating.match(node) and i + 4 < len(nodes):
        #     content = rm_desc_templ(nodes[i + 4] or nodes[i + 3])
        #     if content and content not in result and content not in stored:
        #         content_to_match.put(content)
        #     continue

    content = ""
    while not date_to_match.empty() and not content_to_match.empty():
        content = content_to_match.get()
        if content not in result:
            result[content] = date_to_match.get()
    return result
