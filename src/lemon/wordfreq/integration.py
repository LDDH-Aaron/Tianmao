from collections import Counter
from typing import Iterable

from .wordc import generate_wordcloud
from .cutter import Cutter, load_stopwords

DEFAULT_STOPWORDS_FILES = (
    "./stopwords/baidu_stopwords.txt",
    "./stopwords/cn_stopwords.txt",
    "./stopwords/hit_stopwords.txt",
    "./stopwords/scu_stopwords.txt",
)


def cut_and_generate(text: str, sw_files: Iterable[str] | None = None):
    sw = (
        load_stopwords(*DEFAULT_STOPWORDS_FILES)
        if sw_files is None
        else load_stopwords(*sw_files)
    )
    cutter = Cutter(sw)
    words = cutter.cut(text)
    cloud = generate_wordcloud(Counter(words))
    return cloud
