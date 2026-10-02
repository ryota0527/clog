import json
from datetime import datetime, timedelta
from collections import defaultdict
from system import LOG


def load_log():
    workhr = []
    with open(LOG, "r", encoding="utf-8") as f:
        data = json.load(f)

    for d in data:
        start_time = datetime.strptime(d["start"], "%Y-%m-%d %H:%M:%S")
        fin_time = datetime.strptime(d["finish"], "%Y-%m-%d %H:%M:%S")
        ctgr = d["category"]
        wh = fin_time - start_time  # working hours: hh:mm:ss (timedelta)

        workhr.append({
                        "start": start_time,
                        "finish": fin_time,
                        "working_hr": wh,
                        "category": ctgr
                    })

    return workhr


def categorize(log_grp):
    categorized_wh = defaultdict(lambda: timedelta())
    for log in log_grp:
        categorized_wh[log["category"]] += log["working_hr"]

    return categorized_wh


def grp_period(period):
    # period = day, week, month, year
    logs = load_log()
    sum = []

    idx = 0
    for i in range(len(logs)-1):
        if period == "day":
            l0 = logs[i]["start"].date()
            l1 = logs[i+1]["start"].date()

        elif period == "week":
            l0 = logs[i]["start"].isocalendar().week
            l1 = logs[i+1]["start"].isocalendar().week
            if l0 != l1:
                sum.append(logs[idx:i+1])
                idx = i+1
            continue

        elif period == "month":
            l0 = logs[i]["start"].month
            l1 = logs[i+1]["start"].month

        elif period == "year":
            l0 = logs[i]["start"].year
            l1 = logs[i+1]["start"].year

        if l1 != l0:
            sum.append(logs[idx:i+1])
            idx = i+1
        else:
            continue

    sum.append(logs[idx:])

    return sum


def total_wh(log_grp):
    total = timedelta()
    for log in log_grp:
        total += log["working_hr"]

    return total
