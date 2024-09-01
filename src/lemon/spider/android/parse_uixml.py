from typing import TypedDict
import re

from lxml import etree


class Rating(TypedDict):
    date: str
    content: str


_regex_date = re.compile(r"(\d{4}年)?\d{1,2}月\d{1,2}日")


def parse(xmltext: str):
    xml = etree.XML(xmltext, etree.XMLParser())
    nodes = [e.attrib.get("content-desc", "") for e in xml.findall(".//node")]

    sus = []
    for i, node in enumerate(nodes):
        if _regex_date.match(node) and i + 1 < len(nodes):
            sus.append((node, nodes[i + 1]))
    return sus
