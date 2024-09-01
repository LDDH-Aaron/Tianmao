import re
import json

import thulac


def cut_with_thlac(text: str, thu: thulac.thulac):
    return [word.strip() for word, _ in thu.cut(text)]


def load_stopwords(*files):
    stopwords: set[str] = set()
    for fn in files:
        with open(fn, "r", encoding="utf-8") as f:
            stopwords.update(line.strip().lower() for line in f)
    return stopwords


_pattern_filter_prompt = re.compile(r"(^|\s)[\u4e00-\u9fa5]{4}：\s*")
try:
    _pattern_emoji = re.compile(r'[\U00010000-\U0010ffff]')
except re.error:
    _pattern_emoji = re.compile(r'[\uD800-\uDBFF][\uDC00-\uDFFF]')

def wash(*texts: str, stopwords: set[str], no_prompt=True):
    return [
        (_pattern_filter_prompt.sub("", text) if no_prompt else text)
        for text in texts
        if text.lower() not in stopwords
        and len(text) > 1
        and not _pattern_emoji.search(text)
    ]


class Cutter:
    def __init__(self, stopwords: set[str]) -> None:
        self._thu = thulac.thulac(seg_only=True)
        self._stopwords = stopwords

    def cut(self, text):
        return wash(*cut_with_thlac(text, self._thu), stopwords=self._stopwords)


if __name__ == "__main__":
    from wordc import generate_wordcloud
    from collections import Counter

    textfile = input("Text file:")
    with open(textfile, "r", encoding="utf-8") as fp:
        text = fp.read()
    sw = load_stopwords(
        "./stopwords/baidu_stopwords.txt",
        "./stopwords/cn_stopwords.txt",
        "./stopwords/hit_stopwords.txt",
        "./stopwords/scu_stopwords.txt",
    )
    cutter = Cutter(sw)
    words = cutter.cut(text)
    generate_wordcloud(Counter(words))
    with open(textfile + ".washed.json", "w+", encoding="utf-8") as fp:
        json.dump(words, fp, ensure_ascii=False, indent=4)
