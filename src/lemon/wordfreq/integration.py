from collections import Counter
import json

import matplotlib.pyplot as plt

from wordc import generate_wordcloud
from cutter import Cutter, load_stopwords

DEFAULT_STOPWORDS_FILES = (
    "./stopwords/baidu_stopwords.txt",
    "./stopwords/cn_stopwords.txt",
    "./stopwords/hit_stopwords.txt",
    "./stopwords/scu_stopwords.txt",
)


def cut_and_generate(text: str, sw_files=None):
    sw = (
        load_stopwords(DEFAULT_STOPWORDS_FILES)
        if sw_files is None
        else load_stopwords(*sw_files)
    )
    cutter = Cutter(sw)
    words = cutter.cut(text)
    cloud = generate_wordcloud(Counter(words))
    return cloud


if __name__ == "__main__":
    textfile = input("Text file:")
    with open(textfile, "r", encoding="utf-8") as fp:
        txt = (
            "\n".join([i["content"] for i in json.load(fp)])
            if textfile.endswith(".json")
            else fp.read()
        )
    c = cut_and_generate(txt)

    plt.figure(figsize=(16, 9))
    plt.imshow(c, interpolation="bilinear")
    plt.axis("off")
    plt.show()
