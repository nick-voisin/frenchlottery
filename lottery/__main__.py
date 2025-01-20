import argparse
from lottery import get_euromillions_results, get_loto_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="lottery", description="Quickly retrieve lottery results", epilog="Lottery Results"
    )

    parser.add_argument("-s", "--source", help="Source")
    parser.add_argument("-n", "--lines", help="Output the last lines")
    args = parser.parse_args()

    source = args.source
    lines = args.lines

    match args.source:
        case "euro":
            res = get_euromillions_results()
        case "loto":
            res = get_loto_results()
        case _:
            raise ValueError("Invalid source: either 'euro' or 'loto'")

    if lines:
        print(res.tail(int(lines)))
    else:
        print(res)
