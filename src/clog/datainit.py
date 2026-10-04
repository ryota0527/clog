from clog.system import DATA_DIR, CATEGORY, START_LOG, LOG
import json


def init(args):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if LOG.exists():
        ask = input("Session records exist. Are you sure to initialize again? [y/n]")
        if ask == "y":
            with open(LOG, "w", encoding="utf-8") as h:
                json.dump([], h, indent=4)
        elif ask == "n":
            return
        else:
            print("error: invalid answer")
            return
    else:
        with open(LOG, "w", encoding="utf-8") as h:
            json.dump([], h, indent=4)

    with open(CATEGORY, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

    with open(START_LOG, "w", encoding="utf-8") as g:
        json.dump([], g, indent=4)

    print("initialized")
