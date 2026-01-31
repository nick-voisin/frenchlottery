from pathlib import Path
import polars as pl

from frenchlottery.constants import LOTO_URLS
from frenchlottery.helper import LotterySource, download_zipfile, format_dataframe


def format_dataframes(raw_dataframes: list[pl.DataFrame]) -> pl.DataFrame:
    """
    Applies the 'format_dataframe' function to provided list of dataframes 'raw_dataframes',
    and concatenates them into one dataframe.

    Args:
        raw_dataframes (List[pd.DataFrame]): Dataframes provided from Zip Archive extraction.

    Returns:
        pd.DataFrame: Clean formatted dataframe.
    """
    # Format dataframes with date format : dd/mm/yyyy
    dfs = [format_dataframe(df, source=LotterySource.LOTO) for df in raw_dataframes]
    concatenated_dataframe = pl.concat(dfs)
    concatenated_dataframe = concatenated_dataframe.sort("date")

    return concatenated_dataframe


def generate_loto_results() -> pl.DataFrame:
    """
    Gets all the historical results of the French lottery from 2004 onwards into a pandas DataFrame.
    Data is downloaded from the 'Française des Jeux' website: 'https://www.fdj.fr/'.

    Returns:
        pd.DataFrame: DataFrame of historical results of the French lottery.
    """

    raw_dataframes = [download_zipfile(url, source=LotterySource.LOTO) for url in list(LOTO_URLS.values())[:-1]]
    formatted_dataframe = format_dataframes(raw_dataframes)
    return formatted_dataframe

def get_last_loto_results() -> pl.DataFrame:
    """
    Returns the last results of the French lottery i.e. from 2019 and onwards into a polars DataFrame.
    Data is downloaded from the 'Francaise des Jeux' website.

    Returns:
        pl.DataFrame: Loto historical results.
    """

    raw_dataframe = download_zipfile(list(LOTO_URLS.values())[-1], source=LotterySource.LOTO)
    formatted_dataframe = format_dataframe(raw_dataframe, source=LotterySource.LOTO)
    return formatted_dataframe


def get_full_loto_results() -> pl.DataFrame:
    """
    Gets all the historical results of the Euromillions lottery from 2004 onwards into a polars DataFrame.
    Data is downloaded from the 'Francaise des Jeux' website.

    Returns:
        pl.DataFrame: Euromillions historical results.
    """

    # read stored csv file from data folder, already formatted
    data_folder = Path(__file__).parent / "data"
    historical_data = pl.read_csv(data_folder / "loto_2008_2019.csv", separator=",")
    last_data = get_last_loto_results()
    formatted_dataframe = pl.concat([historical_data, last_data]).sort("date")
    return formatted_dataframe