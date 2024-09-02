import subprocess
import json
import time
import random

import uiautomator2 as u2

from parse_uixml import parse_ratingpage


def run_command(*args):
    return subprocess.run(
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).returncode


def dump(tofile="./ui.xml"):
    run_command("adb", "shell", "uiautomator", "dump", "/sdcard/view.xml")
    run_command("adb", "pull", "/sdcard/view.xml", tofile)


def update_no_override(dst: dict, src: dict):
    dst.update({k: v for k, v in src.items() if k not in dst})


def main():
    while True:
        try:
            print("连接设备...")
            device = u2.connect()
        except u2.ConnectError as e:
            print("连接设备失败：", e)
            input("按Enter重试")
        else:
            break
    result: dict[str, str] = {}
    input("就绪。请手动将页面导航至评价列表，然后按下Enter")
    try:
        # tmpfile = "./ui.xml"
        cycle = 0
        no_increase_count = 0
        while True:
            # dump(tmpfile)
            size = len(result)
            # with open(tmpfile, "rb") as fp:
            #     data = parse(fp.read(), stored=result)
            data = parse_ratingpage(device.dump_hierarchy().encode("utf-8"), stored=result)
            print(*data.items(), sep="\n")
            update_no_override(result, data)
            cycle += 1
            # run_command(
            #     "adb",
            #     "shell",
            #     "input",
            #     "swipe",
            #     str(random.randint(480, 600)),
            #     str(1500 + random.randint(-10, 10)),
            #     str(random.randint(480, 600)),
            #     str(1000 + random.randint(-10, 10)),
            # )
            device.swipe(
                random.randint(480, 600),
                1500 + random.randint(-10, 10),
                random.randint(480, 600),
                1000 + random.randint(-10, 10),
            )

            print("Cycle:", cycle, " Add:", len(result) - size, " Total:", len(result))

            if len(result) == size:
                no_increase_count += 1
            else:
                no_increase_count = 0
            if no_increase_count > 10:
                break
            # time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    print(len(result), "ratings in total, saving...")
    with open(f"./result_{int(time.time())}.json", "w+", encoding="utf-8") as wfp:
        json.dump(
            [{"date": v, "content": k} for k, v in result.items()],
            wfp,
            ensure_ascii=False,
            indent=4,
        )
    print("saved!")


# if __name__ == "__main__":
#     main()
