from euromillions import EuromillionResults

results = EuromillionResults()

results.export()

df = results.original_data

print(df)
