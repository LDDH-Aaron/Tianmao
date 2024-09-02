from wordcloud import WordCloud
from collections import Counter


def generate_wordcloud(word_freq: Counter, output_path: str | None = None):
    wordcloud = WordCloud(
        font_path="simhei.ttf",  # 显示中文
        width=1600,
        height=900,
        background_color="white",
    ).generate_from_frequencies(word_freq)
    if output_path:
        wordcloud.to_file(output_path)
    return wordcloud
