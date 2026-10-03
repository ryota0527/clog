import argparse
import clog.log as log
import clog.tui as tui
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

    addctgr_parser = subparsers.add_parser(
        "add",
        help="add a category"
    )
    addctgr_parser.add_argument(
        "category",
        help="category name"
    )
    addctgr_parser.set_defaults(func=log.add_category)

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

    args = parser.parse_args()

    args.func(args)
