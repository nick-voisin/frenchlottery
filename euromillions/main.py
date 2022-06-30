from euromillions.results import get_results

if __name__ == "__main__":
    res = get_results()
    print(res.tail(5))
