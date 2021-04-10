from dataclasses import dataclass, field

from pandas.io.pytables import IndexCol
from lottery.helper.pandas_helper import loop
from lottery.helper.file_helper import download_zipped_file, save_zipped_file
import os
from typing import List, Any, Optional
from datetime import datetime
import pandas as pd
from pathlib import Path


EUROMILLIONS_ORIGINAL_PATH = Path(os.path.abspath(__file__)).parents[1] / "data" / "euromillions" / "original"
EUROMILLIONS_FORMATTED_PATH = Path(os.path.abspath(__file__)).parents[1] / "data" / "euromillions" / "formatted"


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
        values = [self.date]
        return values + self.balls + self.stars


class EuromillionResults:

    def __init__(self, force: bool = False):
        self.draws: Optional[List[EuromillionDraw]] = []
        self.original_data: Optional[pd.DataFrame] = None
        self.is_sorted: bool = False
        self.is_loaded: bool = False
        self.is_formatted: bool = False

        self._launch(force_download=force)

    def __str__(self):
        if self.is_formatted:
            for draw in self.draws:
                print(draw)

    def __getitem__(self, key) :
        return self.draws[key]
        

    def _is_data_local(self) -> bool:
        files = [file_path for file_path in EUROMILLIONS_ORIGINAL_PATH.glob('*.csv') ]
        if len(files) >= 6:
            self.is_loaded = True
            return True
        else:
            return False

    def _download_files(self) -> None:
        urls = [
            "https://media.fdj.fr/static/csv/euromillions/euromillions_200402.zip",
            "https://media.fdj.fr/static/csv/euromillions/euromillions_201105.zip",
            "https://media.fdj.fr/static/csv/euromillions/euromillions_201402.zip",
            "https://media.fdj.fr/static/csv/euromillions/euromillions_201609.zip",
            "https://media.fdj.fr/static/csv/euromillions/euromillions_201902.zip",
            "https://media.fdj.fr/static/csv/euromillions/euromillions_202002.zip"
        ]

        for index, url in enumerate(urls):
            zipped_file = download_zipped_file(url)
            save_zipped_file(zipped_file, EUROMILLIONS_ORIGINAL_PATH, f"euromillions_{index+1}.csv")
        
        self.is_loaded = True


    def _load_files_to_dataframe_list(self) -> List[pd.DataFrame]:
        path = EUROMILLIONS_ORIGINAL_PATH
        return [pd.read_csv(file_path, sep=";", index_col=False) for file_path in path.glob('*.csv')]


    def _format_dataframe(self, df: pd.DataFrame, date_format="%d/%m/%Y") -> pd.DataFrame:
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
        # exception for first file
        head_df = self._format_dataframe(df=df_list[0], date_format="%Y%m%d")
        tail_dfs = [self._format_dataframe(df) for df in df_list[1:]]
        formatted_dfs = [head_df]
        formatted_dfs.extend(tail_dfs)
        return formatted_dfs

    def _load(self, force: bool = False) -> None:
        if force:
            self._download_files()
        else:
            if self.is_loaded or self._is_data_local():
                return
            else:
                self._download_files()

    def _format(self) -> None:
        if self.is_formatted:
            return

        if self.is_loaded:
            raw_dataframes = self._load_files_to_dataframe_list()
            formatted_dataframe = self._format_dataframe_list(raw_dataframes)
            self.original_data = pd.concat(formatted_dataframe, axis=0)
            for row in loop(self.original_data):
                balls, stars = [row.B1, row.B2, row.B3, row.B4, row.B5], [row.S1, row.S2]
                draw = EuromillionDraw(date=row.Date, balls=balls, stars=stars)
                self.draws.append(draw)
            self.is_formatted = True
        else:
            raise Exception("Please download data beforehand via load.")

    def _launch(self, force_download: bool = False) -> None:
        self._load(force_download)
        self._format()


    def sort(self) -> None:
        for draw in self.draws:
            draw.sort()


    def to_dataframe(self) -> Optional[pd.DataFrame]:
        if self.is_formatted:
            results = [draw.to_list() for draw in self.draws]
            df = pd.DataFrame(results, columns=["Date", "B1", "B2", "B3", "B4", "B5", "S1", "S2"])
            df.set_index("Date", inplace=True)
            return df
        else:
            return None


    def export(self, folder_path: Path = None) -> None:
        if self.is_formatted:
            path = EUROMILLIONS_FORMATTED_PATH if folder_path is None else folder_path
            path = path / "euromillions.csv"
            self.to_dataframe().to_csv(path, sep=";")
        else:
            return None




