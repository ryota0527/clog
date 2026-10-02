import argparse
import clog.log as log
import clog.tui as tui


def main():
    parser = argparse.ArgumentParser(
        prog="clog"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    addctgr_parser = subparsers.add_parser(
        "add",
        help="add a category"
    )
    addctgr_parser.set_defaults(func=log.add_category)

    start_parser = subparsers.add_parser(
        "start",
        help="start a session"
    )
    start_parser.set_defaults(func=log.start)

    stop_parser = subparsers.add_parser(
        "stop",
        help="stop current session"
    )
    stop_parser.set_defaults(func=log.stop)

    show_parser = subparsers.add_parser(
        "show",
        help="show reports"
    )
    show_parser.set_defaults(func=tui.show)

    args = parser.parse_args()

    args.func(args)
