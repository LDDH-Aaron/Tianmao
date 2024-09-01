import subprocess
import json
import time
import random


from parse_uixml import parse


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
    result: dict[str, str] = {}
    try:
        tmpfile = "./ui.xml"
        cycle = 0
        no_increase_count = 0
        while True:
            dump(tmpfile)
            size = len(result)
            with open(tmpfile, "rb") as fp:
                data = parse(fp.read(), stored=result)
            print(*data.items(), sep="\n")
            update_no_override(result, data)
            cycle += 1
            run_command(
                "adb",
                "shell",
                "input",
                "swipe",
                str(random.randint(480, 600)),
                str(1500 + random.randint(-10, 10)),
                str(random.randint(480, 600)),
                str(1000 + random.randint(-10, 10)),
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


if __name__ == "__main__":
    main()
