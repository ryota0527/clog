from system import DATA_DIR, CATEGORY, START_LOG, LOG
import json


DATA_DIR.mkdir(parents=True, exist_ok=True)

with open(CATEGORY, "w", encoding="utf-8") as f:
    json.dump([], f, indent=4)

with open(START_LOG, "w", encoding="utf-8") as g:
    json.dump([], g, indent=4)

with open(LOG, "w", encoding="utf-8") as h:
    json.dump([], h, indent=4)
