import pandas as pd

from frenchlottery.helper import download_zipfile

# see https://www.fdj.fr/jeux-de-tirage/loto/historique
LOTO_URLS = [
    # 2008 - 2017
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afm6",
    # 2017 - 2019
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afn6",
    # 2019
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afo6",
    # 2019 - 2025
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afp6",
]


def format_dataframe(raw_df: pd.DataFrame, date_format: str = "%d/%m/%Y") -> pd.DataFrame:
    """Formats a dataframe extracted from a zip archive, to the following format :
    Date | B1 | B2 | B3 | B4 | B5 | S1, where Bi represents the ball number and Si the star number.
    The returned dataframe is also indexed by date.

    Args:
        raw_df (pd.DataFrame): Raw dataframe extracted from the zip archive.
        date_format (str, optional): Date format of index. Defaults to "%d/%m/%Y".

    Returns:
        pd.DataFrame: Formatted dataframe.
    """
    columns_mapping = {
        "date_de_tirage": "Date",
        "boule_1": "B1",
        "boule_2": "B2",
        "boule_3": "B3",
        "boule_4": "B4",
        "boule_5": "B5",
        "numero_chance": "S1",
    }

    df = raw_df.copy()
    df = df[columns_mapping.keys()]
    df = df.rename(columns=columns_mapping)
    df["Date"] = pd.to_datetime(df["Date"], format=date_format)
    return df.set_index("Date")


def format_dataframes(raw_dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Applies the 'format_dataframe' function to provided list of dataframes 'raw_dataframes',
    and concatenates them into one dataframe.

    Args:
        raw_dataframes (List[pd.DataFrame]): Dataframes provided from Zip Archive extraction.

    Returns:
        pd.DataFrame: Clean formatted dataframe.
    """
    # Format other dataframes with date format : dd/mm/yyyy
    dfs = [format_dataframe(df) for idx, df in enumerate(raw_dataframes)]

    # concatenate along index and sort.
    concatenated_dataframe = pd.concat(dfs, axis=0)
    concatenated_dataframe.sort_index(inplace=True)

    return concatenated_dataframe


def get_loto_results() -> pd.DataFrame:
    """
    Gets all the historical results of the French lottery from 2004 onwards into a pandas DataFrame.
    Data is downloaded from the 'Française des Jeux' website: 'https://www.fdj.fr/'.

    Returns:
        pd.DataFrame: DataFrame of historical results of the French lottery.
    """

    raw_dataframes = [download_zipfile(url) for url in LOTO_URLS]
    formatted_dataframe = format_dataframes(raw_dataframes)
    return formatted_dataframe
