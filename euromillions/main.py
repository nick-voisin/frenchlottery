from euromillions import EuromillionResults

results = EuromillionResults()

results.export()

df = results.to_dataframe()

results.sort()

df_sorted = results.to_dataframe()
