import subprocess
import json
import time


def dump(tofile="./ui.xml"):
    subprocess.run(
        ["adb", "shell", "uiautomator", "dump", "/sdcard/view.xml"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    subprocess.run(
        ["adb", "pull", "/sdcard/view.xml", tofile],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


if __name__ == "__main__":
    from parse_uixml import parse

    result = set()
    try:
        tmpfile = "./ui.xml"
        cycle = 0
        while True:
            dump(tmpfile)
            with open(tmpfile, "rb") as fp:
                data = parse(fp.read())
                print("obtained:", data)
            result.update(data)
            cycle += 1
            print("Cycle", cycle)
    except KeyboardInterrupt:
        pass
    print("saving...")
    with open(f"./result_{int(time.time())}.json", "w+", encoding="utf-8") as wfp:
        json.dump(list(result), wfp, ensure_ascii=False, indent=4)
