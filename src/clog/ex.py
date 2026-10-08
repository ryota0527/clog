import argparse
import clog.log as log
import clog.tui as tui
from clog.statistics import fill_blanc
import clog.datainit as init


def main():
    parser = argparse.ArgumentParser(
        prog="clog"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    init_parser = subparsers.add_parser(
        "init",
        help="initialize"
    )
    init_parser.set_defaults(func=init.init)

    crectgr_parser = subparsers.add_parser(
        "create",
        help="create a category"
    )
    crectgr_parser.add_argument(
        "category",
        help="category name"
    )
    crectgr_parser.set_defaults(func=log.add_category)

    list_parser = subparsers.add_parser(
            "list",
            help="list existing cateogies"
    )
    list_parser.set_defaults(func=log.list_ctgr)

    start_parser = subparsers.add_parser(
        "start",
        help="start a session"
    )
    start_parser.add_argument(
        "category",
        help="category name"
    )
    start_parser.set_defaults(func=log.start)

    stop_parser = subparsers.add_parser(
        "stop",
        help="stop current session"
    )
    stop_parser.set_defaults(func=log.fin)

    show_parser = subparsers.add_parser(
        "show",
        help="show reports"
    )
    show_parser.set_defaults(func=tui.show)

    add_parser = subparsers.add_parser(
        "add",
        help="add working time"
    )
    add_parser.add_argument(
        "category",
        help="category name"
    )
    add_parser.add_argument(
        "working_time",
        help="working time [hr]"
    )
    add_parser.set_defaults(func=log.add)

    args = parser.parse_args()

    fill_blanc()
    args.func(args)
