from pathlib import Path
from lottery import get_euromillions_results, get_loto_results
import numpy as np

if __name__ == "__main__":
    data_folder = Path(__file__).parents[1] / "data"
    # euromillions_res = get_euromillions_results()
    # euromillions_res.to_csv(data_folder / "eur_results_1.csv")

    data_folder = Path(__file__).parents[1] / "data"
    loto_res = get_loto_results()
    loto_res.to_csv(data_folder / "loto.csv")

    print(loto_res.tail(10))

    sorted_loto = loto_res[["B1", "B2", "B3", "B4", "B5"]].apply(np.sort, axis=1, raw=True)
    sorted_loto["S1"] = loto_res["S1"]
    sorted_loto.to_csv(data_folder / "loto_sorted.csv")