from rich.console import Console, Group
from rich.layout import Layout
from rich.align import Align
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime, timedelta
import clog.statics as st


def show_bar(hr, max_hr):
    hr = hr.total_seconds() / 3600
    max_hr = max_hr.total_seconds() / 3600

    if max_hr == 0:
        return None

    n = int(hr / max_hr * 20)
    return Text("■" * n, style="green")


def ctgr_table(log_by_category, total_wh):
    table_c = Table(
        show_header=False
    )

    whs = []
    for key, val in log_by_category.items():
        hours = val.total_seconds() / 3600
        r = hours / total_wh * 100
        whs.append({
                   "wh": hours,
                   "r": r,
                   "ctgr": key
        })

    whs_sorted = sorted(
            whs,
            key=lambda x: x["wh"],
            reverse=True
    )

    for i, wh in enumerate(whs_sorted):
        if i == 5:
            wh_other = 0
            r_other = 0
            for j in whs_sorted[i:]:
                wh_other += j["wh"]
                r_other += j["r"]

            table_c.add_row("Others", Text(f"{round(wh_other, 1)} h ({round(r_other, 1)}%)", style="green"))
            break

        else:
            table_c.add_row(wh["ctgr"], Text(f"{round(wh["wh"], 1)} h ({round(wh["r"], 1)}%)", style="green"))

    return table_c


def show(args):
    console = Console(width=90, height=40)

    layout = Layout()

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="summary")
    )

    layout["summary"].split_row(
        Layout(name="day&week", ratio=1),
        Layout(name="month&year", ratio=1)
    )

    layout["day&week"].split_column(
            Layout(name="today", ratio=3),
            Layout(name="week", ratio=5)
    )

    layout["month&year"].split_column(
            Layout(name="month", ratio=1),
            Layout(name="year", ratio=1)
    )

    # header section
    title = Text()
    title.append("● ", style="bold bright_green")
    title.append("CLOG", style="bold bright_cyan")
    title.append("  |  ")
    title.append("DASHBOARD", style="bold white")

    layout["header"].update(
        Panel(
            Align.center(title, vertical="middle"),
            border_style="bright_cyan",
            padding=(0, 1),
        )
    )

    # daily section
    daily = st.grp_period("day")
    if daily == []:
        total_day = 0
    else:
        total_day = st.total_wh(daily[-1]).total_seconds() / 3600
        day_by_category = st.categorize(daily[-1])

    if len(daily) > 1:
        total_yesterday = st.total_wh(daily[-2]).total_seconds() / 3600
    else:
        total_yesterday = 0

    if total_day != 0:
        table_c_day = ctgr_table(day_by_category, total_day)
    else:
        table_c_day = Table(show_header=False)

    layout["today"].update(
        Panel(
            Group(
                Text(""),
                Text(f"Total: {round(total_day, 1)} h  (Yesterday: {round(total_yesterday, 1)} h)",
                     style="bold bright_white"),
                Text(""),
                table_c_day
            ),
            title=Text(f"Daily Report ({datetime.today().strftime("%Y-%m-%d")})", style="bold white"),
            border_style="bright_black"
        )
    )

    # weekly section
    weekly = st.grp_period("week")
    if weekly == []:
        total_wek = 0
    else:
        thisweek = weekly[-1]
        if thisweek == []:
            total_wek = 0
        else:
            total_wek = st.total_wh(thisweek).total_seconds() / 3600
            wek_by_category = st.categorize(thisweek)

    if len(weekly) > 1:
        total_lastwek = st.total_wh(weekly[-2]).total_seconds() / 3600
    else:
        total_lastwek = 0

    table_wek = Table(
        show_header=False,
    )

    if total_wek != 0:
        table_wek.add_column("day")
        table_wek.add_column("bar")
        table_wek.add_column("hr")

        weekday_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        perday = st.grp_period("day", thisweek)
        daily_total = [st.total_wh(logs) for logs in perday]
        max_hr = max(daily_total, default=timedelta())

        start_weekday = perday[0][0]["start"].weekday()
        end_weekday = perday[-1][0]["start"].weekday() + 1
        for d in weekday_list[:start_weekday]:
            table_wek.add_row(
                    d,
                    None,
                    "0"
            )

        for d, wh in zip(weekday_list[start_weekday:end_weekday], daily_total):
            table_wek.add_row(
                    d,
                    show_bar(wh, max_hr),
                    str(round((wh.total_seconds() / 3600), 1))
            )

        for d in weekday_list[end_weekday:]:
            table_wek.add_row(
                    d,
                    None,
                    "0"
            )

        table_c_wek = ctgr_table(wek_by_category, total_wek)

    else:
        table_c_wek = Table(show_header=False)

    layout["week"].update(
        Panel(
            Group(
                Text(""),
                Text(f"Total : {round(total_wek, 1)} h  (Last week: {round(total_lastwek, 1)} h)",
                     style="bold bright_white"),
                Text(""),
                table_wek,
                Text(""),
                table_c_wek
            ),
            title=Text("Weekly Reports", style="bold white"),
            border_style="bright_black"
        )
    )

    # monthly section
    monthly = st.grp_period("month")
    if monthly == []:
        total_mon = 0
        av_perday = 0
    else:
        thismonth = monthly[-1]
        if thismonth == []:
            total_mon = 0
            av_perday = 0
        else:
            total_mon = st.total_wh(thismonth).total_seconds() / 3600
            mon_by_category = st.categorize(thismonth)
            av_perday = st.ave_wh_perday(thismonth)

    if len(monthly) > 1:
        total_lastmon = st.total_wh(monthly[-2]).total_seconds() / 3600
    else:
        total_lastmon = 0

    if total_mon != 0:
        table_c_mon = ctgr_table(mon_by_category, total_mon)
    else:
        table_c_mon = Table(show_header=False)

    layout["month"].update(
        Panel(
            Group(
                Text(""),
                Text(f"Total: {round(total_mon, 1)} h  (Last month: {round(total_lastmon, 1)} h)",
                     style="bold bright_white"),
                Text(""),
                table_c_mon,
                Text(""),
                Text(f"Average per day: {av_perday} h", style="bold bright_white")
            ),
            title=Text(f"Monthly Reports ({datetime.today().strftime("%B")})", style="bold white"),
            border_style="bright_black"
        )
    )

    # yearly section
    yearly = st.grp_period("year")
    if yearly == []:
        total_y = 0
        av_perday = 0
    else:
        thisyear = yearly[-1]
        if thisyear == []:
            total_y = 0
            av_perday = 0
        else:
            total_y = st.total_wh(thisyear).total_seconds() / 3600
            y_by_category = st.categorize(thisyear)
            av_perday = st.ave_wh_perday(thisyear)

    if len(yearly) > 1:
        total_ly = st.total_wh(yearly[-2]).total_seconds() / 3600
    else:
        total_ly = 0

    if total_y != 0:
        table_c_y = ctgr_table(y_by_category, total_y)
    else:
        table_c_y = Table(show_header=False)

    layout["year"].update(
        Panel(
            Group(
                Text(""),
                Text(f"Total: {round(total_y, 1)} h  (Last year: {round(total_ly, 1)} h)",
                     style="bold bright_white"),
                Text(""),
                table_c_y,
                Text(""),
                Text(f"Average per day: {av_perday} h", style="bold bright_white")
            ),
            title=Text(f"Yearly Reports ({datetime.today().strftime("%Y")})", style="bold white"),
            border_style="bright_black"
        )
    )

    console.print(layout)
