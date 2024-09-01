from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter


def generate_wordcloud(word_freq: Counter, output_path: str | None = None):
    wordcloud = WordCloud(
        font_path="simhei.ttf",  # 显示中文
        width=1600,
        height=900,
        background_color="white",
    ).generate_from_frequencies(word_freq)
    plt.figure(figsize=(16, 9))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    if output_path:
        wordcloud.to_file(output_path)
    plt.show()
