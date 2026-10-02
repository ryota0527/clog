import json
from datetime import datetime
from system import CATEGORY, START_LOG, LOG


def start(arg):
    with open(START_LOG, "r", encoding="utf-8") as f:
        start_log = json.load(f)

    if start_log != []:
        print("error: current session has not finished.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CATEGORY, "r", encoding="utf-8") as g:
        ctgr = json.load(g)

    if arg not in ctgr:
        raise ValueError("error: category not found.")

    data = {
                "datetime": timestamp,
                "category": arg,
            }

    with open(START_LOG, "w", encoding="utf-8") as h:
        json.dump(data, h, ensure_ascii=False, indent=4)


def fin():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(START_LOG, "r", encoding="utf-8") as f:
        start_log = json.load(f)

    if len(start_log) == 0:
        print("error: start timestamp does not exist.")
        return

    data = {
                "start": start_log["datetime"],
                "finish": timestamp,
                "category": start_log["category"]
            }

    with open(LOG, "r", encoding="utf-8") as g:
        datalist = json.load(g)

    datalist.append(data)

    with open(LOG, "w", encoding="utf-8") as h:
        json.dump(datalist, h, ensure_ascii=False, indent=4)

    with open(START_LOG, "w", encoding="utf-8") as i:
        json.dump([], i, ensure_ascii=False, indent=4)


def add_category(arg):
    with open(CATEGORY, "r", encoding="utf-8") as f:
        ctgr = json.load(f)

    if arg in ctgr:
        raise ValueError(f"error: category {arg} already exists.")

    ctgr.append(arg)

    with open(CATEGORY, "w", encoding="utf-8") as g:
        json.dump(ctgr, g, ensure_ascii=False, indent=4)
