import argparse

from frenchlottery import get_last_results, get_full_results
from frenchlottery.domain import get_source_from_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="frenchlottery", description="Quickly retrieve lottery results", epilog="Lottery Results From FDJ"
    )

    parser.add_argument("-s", "--source", default="loto", help="Source", choices=["loto", "euro"])
    parser.add_argument("-n", "--lines", help="Output the last lines")
    parser.add_argument("-f", "--full", action="store_true", help="Output full results")

    parsed_args = parser.parse_args()

    source = get_source_from_code(parsed_args.source)
    if parsed_args.full:
        data = get_full_results(source)
    else:
        data = get_last_results(source)

    if parsed_args.lines:
        print(data.tail(int(parsed_args.lines)))
    else:
        print(data)
