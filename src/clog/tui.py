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
    n = int(hr / max_hr * 20)
    return Text("■" * n, style="green")


def show(args):
    console = Console(width=100, height=40)

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
            Layout(name="today", ratio=1),
            Layout(name="week", ratio=4)
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
    total_day = st.total_wh(daily[-1]).total_seconds() / 3600
    day_by_category = st.categorize(daily[-1])

    grid = Table.grid()

    for key, val in day_by_category.items():
        hours = round(val.total_seconds() / 3600, 1)
        grid.add_row(key, Text(f" {hours} h", style="green"))

    layout["today"].update(
        Panel(
            Group(
                Text(f"Total: {str(round(total_day, 1))} h",
                     style="bold bright_white"),
                Text(""),
                grid
            ),
            title=f"Daily Report ({datetime.today().strftime("%Y-%m-%d")})",
            border_style="bright_black"
        )
    )

    # weekly section
    weekly = st.grp_period("week")
    thisweek = weekly[-1]
    total_wek = round(st.total_wh(thisweek).total_seconds() / 3600, 1)
    wek_by_category = st.categorize(thisweek)

    table_wek = Table(
        show_header=False,
    )

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

    table_wek_c = Table(
        show_header=False
    )

    for key, val in wek_by_category.items():
        hours = round(val.total_seconds() / 3600, 1)
        table_wek_c.add_row(key, Text(f"{hours} h", style="green"))

    layout["week"].update(
        Panel(
            Group(
                Text(f"Total : {total_wek} h",
                     style="bold bright_white"),
                Text(""),
                table_wek,
                Text(""),
                table_wek_c
            ),
            title="Weekly Reports",
            border_style="bright_black"
        )
    )

    # monthly section
    monthly = st.grp_period("month")
    thismonth = monthly[-1]
    total_mon = round(st.total_wh(thismonth).total_seconds() / 3600, 1)
    mon_by_category = st.categorize(thismonth)

    table_mon_c = Table(
        show_header=False
    )

    for key, val in mon_by_category.items():
        hours = round(val.total_seconds() / 3600, 1)
        table_mon_c.add_row(key, Text(f"{hours} h", style="green"))

    layout["month"].update(
        Panel(
            Group(
                Text(f"Total: {total_mon} h",
                     style="bold bright_white"),
                Text(""),
                table_mon_c
            ),
            title=f"Monthly Reports ({thismonth[0]["start"].strftime("%B")})",
            border_style="bright_black"
        )
    )

    # yearly section
    yearly = st.grp_period("year")
    thisyear = yearly[-1]
    total_y = round(st.total_wh(thisyear).total_seconds() / 3600, 1)
    y_by_category = st.categorize(thisyear)

    table_y_c = Table(show_header=False)

    for key, val in y_by_category.items():
        hours = round(val.total_seconds() / 3600, 1)
        table_y_c.add_row(key, Text(f"{hours} h", style="green"))

    layout["year"].update(
        Panel(
            Group(
                Text(f"Total: {total_y} h",
                     style="bold bright_white"),
                Text(""),
                table_y_c
            ),
            title=f"Yearly Reports ({thisyear[0]["start"].strftime("%Y")})",
            border_style="bright_black"
        )
    )

    console.print(layout)
