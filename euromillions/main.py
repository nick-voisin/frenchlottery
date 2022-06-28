from euromillions import EuromillionResults


if __name__ == "main":
    results = EuromillionResults()
    results.export()
    df = results.to_dataframe()
    results.sort()
    df_sorted = results.to_dataframe()
