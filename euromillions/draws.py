import os
from datetime import datetime
from typing import List, Any, Optional, Union
from dataclasses import dataclass, field

import pandas as pd
from pathlib import Path

from euromillions.helper import download_data, loop, valid_or_current_path

# Constants
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

    def __getitem__(self, key: int):
        return self.draws[key] if key < len(self.draws) else self.draws[-1]

    def _download(self, force_download: bool = False) -> None:
        if force_download or not self._is_downloaded:
            try:
                for index, url in enumerate(EUROMILLIONS_URLS):
                    file_name = f"euromillions_{index+1}.csv"
                    download_data(url, EUROMILLIONS_ORIGINAL_PATH, file_name)
                self._is_downloaded = True
            except Exception as e:
                raise RuntimeError("Unable to download data.") from e

    def _format_dataframe(self, df: pd.DataFrame, date_format: str = "%d/%m/%Y") -> pd.DataFrame:
        selected_columns = [
            "date_de_tirage",
            "boule_1",
            "boule_2",
            "boule_3",
            "boule_4",
            "boule_5",
            "etoile_1",
            "etoile_2",
        ]
        
        mapper = {
            "date_de_tirage": "Date",
            "boule_1": "B1",
            "boule_2": "B2",
            "boule_3": "B3",
            "boule_4": "B4",
            "boule_5": "B5",
            "etoile_1": "S1",
            "etoile_2": "S2"
            }
        
        df = df[selected_columns]
        df.rename(columns=mapper, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"], format=date_format)
        df.set_index("Date", inplace=True)
        df.sort_index(inplace=True)
        return df

    def _format_dataframe_list(self, df_list: List[pd.DataFrame]) -> List[pd.DataFrame]:
        # Date format for first file is YYYYMMDD
        first_df = self._format_dataframe(df=df_list[0], date_format="%Y%m%d")

        # Reformat the first date for the 3rd file only
        date = df_list[2].at[0, "date_de_tirage"]
        correct_format = datetime.strptime(date,"%d/%m/%y").strftime("%d/%m/%Y")
        df_list[2].at[0, "date_de_tirage"] = correct_format

        # Process the other of dataframes normally
        rest_dfs = [self._format_dataframe(df) for df in df_list[1:]]
        formatted_dfs = [first_df]
        formatted_dfs.extend(rest_dfs)
        return formatted_dfs

    def _format(self) -> None:
        if not self._is_downloaded:
            raise RuntimeError("Download data before formatting.")
        
        try:
            raw_dataframes = [
                pd.read_csv(file_path, sep=";", index_col=False, encoding="latin-1")
                for file_path in EUROMILLIONS_ORIGINAL_PATH.glob("*.csv")
            ]
            formatted_dataframe = self._format_dataframe_list(raw_dataframes)
            self.original_data = pd.concat(formatted_dataframe, axis=0)
            for row in loop(self.original_data):
                balls, stars = [row.B1, row.B2, row.B3, row.B4, row.B5], [
                    row.S1,
                    row.S2,
                ]
            self.draws.append(EuromillionDraw(date=row.Date, 
                                              balls=balls, 
                                              stars=stars))
        except Exception as e:
            raise Exception("Cannot format data.") from e


    def _launch(self, force_download: bool = False) -> None:
        self._download(force_download)
        self._format()

    def sort(self) -> None:
        for draw in self.draws:
            draw.sort()
        self.is_sorted = True

    def update(self) -> None:
        # get latest data
        latest_url = EUROMILLIONS_URLS[-1]
        file_name = f"euromillions_{len(EUROMILLIONS_URLS)}.csv"
        download_data(latest_url, EUROMILLIONS_ORIGINAL_PATH, file_name)

        # reformat entire dataframe
        self._format()

    def to_dataframe(self) -> pd.DataFrame:
        results = [draw.to_list() for draw in self.draws]
        df = pd.DataFrame(results, columns=["Date", "B1", "B2", "B3", 
                                            "B4", "B5", "S1", "S2"])
        df.set_index("Date", inplace=True)
        return df

    def export(self, folder_path: Optional[Union[Path, str]] = None) -> None:
        path = valid_or_current_path(folder_path)
        self.to_dataframe().to_csv(path, sep=";")
