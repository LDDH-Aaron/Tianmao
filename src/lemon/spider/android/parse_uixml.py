import re
from datetime import datetime
from queue import Queue

from lxml import etree


_regex_date = re.compile(r"(\d{4}年)?\d{1,2}月\d{1,2}日")
_regex_detailed_rating = re.compile(r'昵称([^"]+?)评论([^"]+?)')
_regex_desc_templ = re.compile(r"(^|\s+)[\u4e00-\u9fa5]{4}：")


def rm_desc_templ(rate_content: str):
    return _regex_desc_templ.sub(
        " ", rate_content.removeprefix("商品评价:").removeprefix("评价标题:")
    ).strip()


def parse(xmltext: str, stored: dict[str, str] | None) -> dict[str, str]:
    """
    返回的字典，键为评价内容，值为日期
    
    stored 参数是已经记录的内容，用于去重
    """
    xml = etree.XML(xmltext, etree.XMLParser())
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
            date_to_match.put(date)
            continue
            # date_to_match.put(date)

        if _regex_detailed_rating.match(node) and i + 4 < len(nodes):
            content = rm_desc_templ(nodes[i + 4] or nodes[i + 3])
            if content and content not in result and content not in stored:
                content_to_match.put(content)
            continue

    content = ""
    while not date_to_match.empty() and not content_to_match.empty():
        content = content_to_match.get()
        if content not in result:
            result[content] = date_to_match.get()
    return result
