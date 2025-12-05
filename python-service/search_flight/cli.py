import argparse
import datetime
import webbrowser

from search_flight.core import get_flight_search_urls


def date_type(value: str) -> str:
    try:
        date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        return str(date)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"format isn't correct: {value}. Use format YYYY-MM-DD, ex. 2025-03-28"
        )


def build_parser():
    parser = argparse.ArgumentParser(
        description="Open a browser with pre-filled flight search information."
    )
    parser.add_argument("origin", type=str, help="Origin airport code")
    parser.add_argument("destination", type=str, help="Destination airport code")
    parser.add_argument("date", type=date_type, help="Flight date in YYYY-MM-DD format")
    parser.add_argument(
        "--adults",
        default=2,
        type=int,
        required=False,
        help="Number of adults (default: 2)",
    )
    return parser


def open_flight_search(origin: str, destination: str, date: str, adults: int):
    urls = get_flight_search_urls(origin, destination, date, adults)
    for name in urls:
        webbrowser.open(urls[name])


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    open_flight_search(args.origin, args.destination, args.date, args.adults)


if __name__ == "__main__":
    main()
