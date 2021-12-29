import os
from datetime import datetime
from typing import List, Any, Optional
from dataclasses import dataclass, field

import pandas as pd
from pathlib import Path

from euromillions.helper import loop, download_zipped_file, save_zipped_file


EUROMILLIONS_ORIGINAL_PATH = Path(os.path.abspath(__file__)).parents[0] / "data" / "original"
EUROMILLIONS_FORMATTED_PATH = Path(os.path.abspath(__file__)).parents[0] / "data" / "formatted"
EUROMILLIONS_URLS = [
    "https://media.fdj.fr/static/csv/euromillions/euromillions_200402.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_201105.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_201402.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_201609.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_201902.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_202002.zip",
]


@dataclass
class EuromillionDraw:
    date: datetime
    balls: List[float] = field(default_factory=list)
    stars: List[float] = field(default_factory=list)

    def __str__(self):
        date_str = datetime.strftime(self.date, "%d/%m/%Y")
        balls = [f"B{i} " for i in self.balls]
        stars = [f"*{i} " for i in self.stars]
        return date_str + " - " + "".join(balls) + "".join(stars)

    def sort(self) -> None:
        self.balls.sort()
        self.stars.sort()

    def to_list(self) -> List[Any]:
        return [self.date] + self.balls + self.stars


class EuromillionResults:
    def __init__(self, force_download: bool = False):
        self.draws: Optional[List[EuromillionDraw]] = []
        self.original_data: Optional[pd.DataFrame] = None
        self.is_sorted: bool = False

        self._is_downloaded: bool = False
        self._launch(force_download)

    def __str__(self):
        for draw in self.draws:
            print(draw)

    def __getitem__(self, key):
        return self.draws[key]

    def _download(self, force_download: bool = False) -> None:
        if force_download or not self._is_downloaded:
            for index, url in enumerate(EUROMILLIONS_URLS):
                zipped_file = download_zipped_file(url)
                save_zipped_file(zipped_file, EUROMILLIONS_ORIGINAL_PATH, f"euromillions_{index+1}.csv")
            self._is_downloaded = True

    def _format_dataframe(self, df: pd.DataFrame, date_format: str = "%d/%m/%Y") -> pd.DataFrame:
        formated_df = pd.DataFrame()
        formated_df["Date"] = df["date_de_tirage"]
        formated_df["B1"] = df["boule_1"]
        formated_df["B2"] = df["boule_2"]
        formated_df["B3"] = df["boule_3"]
        formated_df["B4"] = df["boule_4"]
        formated_df["B5"] = df["boule_5"]
        formated_df["S1"] = df["etoile_1"]
        formated_df["S2"] = df["etoile_2"]
        formated_df["Date"] = pd.to_datetime(formated_df["Date"], format=date_format)
        formated_df.set_index("Date", inplace=True)
        formated_df.sort_index(inplace=True)
        return formated_df

    def _format_dataframe_list(self, df_list: List[pd.DataFrame]) -> List[pd.DataFrame]:
        # format date differently for the 1st file
        first_df = self._format_dataframe(df=df_list[0], date_format="%Y%m%d")

        # reformat the first date for the 3rd file only
        df_list[2].at[0, "date_de_tirage"] = datetime.strptime(
            df_list[2].at[0, "date_de_tirage"], "%d/%m/%y"
        ).strftime("%d/%m/%Y")

        rest_dfs = [self._format_dataframe(df) for df in df_list[1:]]
        formatted_dfs = [first_df]
        formatted_dfs.extend(rest_dfs)
        return formatted_dfs

    def _format(self) -> None:
        if self._is_downloaded:
            raw_dataframes = [
                pd.read_csv(file_path, sep=";", index_col=False, encoding="latin-1")
                for file_path in EUROMILLIONS_ORIGINAL_PATH.glob("*.csv")
            ]
            formatted_dataframe = self._format_dataframe_list(raw_dataframes)
            self.original_data = pd.concat(formatted_dataframe, axis=0)
            for row in loop(self.original_data):
                balls, stars = [row.B1, row.B2, row.B3, row.B4, row.B5], [row.S1, row.S2]
                draw = EuromillionDraw(date=row.Date, balls=balls, stars=stars)
                self.draws.append(draw)

    def _launch(self, force_download: bool = False) -> None:
        try:
            self._download(force_download)
            try:
                self._format()
            except Exception as e:
                print(f"Error formatting data: {e}")
        except Exception as e:
            print(f"Error downloading data: {e}")

    def sort(self) -> None:
        for draw in self.draws:
            draw.sort()
        self.is_sorted = True

    def update(self) -> None:
        zipped_file = download_zipped_file(EUROMILLIONS_URLS[-1])
        save_zipped_file(
            zipped_file,
            EUROMILLIONS_ORIGINAL_PATH,
            f"euromillions_{len(EUROMILLIONS_URLS)}.csv",
        )
        self._format()

    def to_dataframe(self) -> pd.DataFrame:
        results = [draw.to_list() for draw in self.draws]
        df = pd.DataFrame(results, columns=["Date", "B1", "B2", "B3", "B4", "B5", "S1", "S2"])
        df.set_index("Date", inplace=True)
        return df

    def export(self, folder_path: Path = None) -> None:
        path = EUROMILLIONS_FORMATTED_PATH if folder_path is None else folder_path
        path = path / "euromillions.csv"
        self.to_dataframe().to_csv(path, sep=";")
