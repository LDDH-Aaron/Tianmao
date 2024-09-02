import json
from matplotlib import pyplot as plt

from wordfreq import cut_and_generate

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
