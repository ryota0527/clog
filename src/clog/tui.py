from rich.console import Console, Group
from rich.layout import Layout
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime, timedelta
import statics as st


def calc_maxhr(log_grp):
    wh0 = timedelta()
    for log in log_grp:
        wh = log["working_hr"]
        if wh > wh0:
            wh0 = wh

    return wh0


def show_bar(hr, max_hr):
    hr = hr.total_seconds() / 3600
    max_hr = max_hr.total_seconds() / 3600
    n = int(hr / max_hr * 20)
    return "█" * n


def show():
    console = Console()

    layout = Layout()

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="today", size=8),
        Layout(name="summary")
    )

    layout["summary"].split_row(
        Layout(name="week", ratio=1),
        Layout(name="month", ratio=1)
    )

    # daily section
    daily = st.grp_period("day")
    total_day = st.total_wh(daily[-1]).total_seconds() / 3600
    day_by_category = st.categorize(daily[-1])

    grid = Table.grid()
    grid.add_row("Total", total_day)
    for key, val in day_by_category.items():
        hours = val.total_seconds() / 3600
        grid.add_row(key, f"{hours: 1f} h")

    layout["today"].update(
            Panel(grid, title=f"Daily Report ({datetime.today()})")
    )

    # weekly section
    weekly = st.grp_period("week")
    thisweek = weekly[-1]
    total_wek = st.total_wh(thisweek).total_seconds() / 3600
    wek_by_category = st.categorize(thisweek)

    table_wek = Table(show_header=False)

    table_wek.add_column("day")
    table_wek.add_column("bar")
    table_wek.add_column("hr")

    weekday_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, d in enumerate(weekday_list):
        max_hr = calc_maxhr(thisweek)
        perday = timedelta()
        for log in thisweek[i]:
            perday += log["working_hr"]

        table_wek.add_row(
                d,
                show_bar(perday, max_hr),
                round((perday.total_seconds() / 3600), 1)
        )

    table_wek_c = Table(show_header=False)

    for key, val in wek_by_category.items():
        hours = val.total_seconds() / 3600
        table_wek_c.add_row(key, f"{hours: 1f} h")

    layout["week"].update(
        Panel(
            Group(
                Text(f"Total : {total_wek} h"),
                Text(""),
                table_wek,
                Text(""),
                table_wek_c
            )
        )
    )

    # monthly section
    """
    monthly = st.grp_period("month")
    thismonth = monthly[-1]
    total_mon = st.total_wh(thismonth).total_seconds() / 3600
    mon_by_category = st.categorize(thismonth)

    table_mon = Table(show_header=False)

    table_mon.add_column("week")
    table_mon.add_column("bar")
    table_mon.add_column("hr")

    for i, d in enumerate():
        max_hr = calc_maxhr(thismonth[i])
        perweek = timedelta()
        for log in thisweek[i]:
            perweek += log["working_hr"]

        table_wek.add_row(
                d,
                show_bar(perday, max_hr),
                round((perday.total_seconds() / 3600), 1)
        )

    table_mon_c = Table(show_header=False)

    for key, val in mon_by_category.items():
        hours = val.total_seconds() / 3600
        table_mon_c.add_row(key, f"{hours: 1f} h")

    layout["month"].update(
        Panel(
            Group(
                Text(f"Total : {total_mon} h"),
                Text(""),
                table_mon,
                Text(""),
                table_mon_c
            )
        )
    )
    """

    console.print(layout)
