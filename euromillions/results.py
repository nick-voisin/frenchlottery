from datetime import datetime
from typing import List

import pandas as pd

from euromillions.helper import download_zipfile


def format_dataframe(raw_df: pd.DataFrame, date_format: str = "%d/%m/%Y") -> pd.DataFrame:
    """Formats a dataframe extracted from a Zip Archive, to the following format :
    Date | B1 | B2 | B3 | B4 | B5 | S1 | S2, where B(i) represents the ball number and S(i) the star number.
    The returned dataframe is also indexed by date.

    Args:
        df (pd.DataFrame): Raw dataframe extracted from the Zip Archive.
        date_format (str, optional): Date format of index. Defaults to "%d/%m/%Y".

    Returns:
        pd.DataFrame: Formatted dataframe.
    """
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
    renamed_columns = ["Date", "B1", "B2", "B3", "B4", "B5", "S1", "S2"]
    mapper = dict(zip(selected_columns, renamed_columns))

    df = raw_df[selected_columns]
    df = df.rename(columns=mapper)
    df.loc[:, "Date"] = pd.to_datetime(df.loc[:, "Date"], format=date_format)
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)
    return df


def format_dataframes(raw_dataframes: List[pd.DataFrame]) -> pd.DataFrame:
    """Applies the 'format_dataframe' function to provided list of dataframes 'raw_dataframes', and concatenates
    them into one dataframe.
    Also performs a slight cleanup of an erroneous date format on the first line of the third dataframe.

    Args:
        raw_dataframes (List[pd.DataFrame]): Dataframes provided from Zip Archive extraction.

    Returns:
        pd.DataFrame: Clean formatted dataframe.
    """
    # Format first dataframe with date format : YYYYMMDD
    first_df = format_dataframe(raw_dataframes[0], date_format="%Y%m%d")

    # Modify date of first row of the third dataframe.
    wrong_date_format = raw_dataframes[2].at[0, "date_de_tirage"]
    correct_date_format = datetime.strptime(wrong_date_format, "%d/%m/%y").strftime("%d/%m/%Y")
    raw_dataframes[2].at[0, "date_de_tirage"] = correct_date_format

    # Format others dataframes with date format : dd/mm/yyyy
    rest_dfs = [format_dataframe(df) for df in raw_dataframes[1:]]
    formatted_dfs = [first_df]
    formatted_dfs.extend(rest_dfs)

    return pd.concat(formatted_dfs, axis=0)


def get_results() -> pd.DataFrame:
    """Gets all the historical results of the Euromillion lottery from 2004 onwards into a pandas DataFrame.
    Data is downloaded from the 'Francaise des Jeux' website.

    Returns:
        pd.DataFrame: Euromillion historical results.
    """

    EUROMILLIONS_URLS = [
        "https://media.fdj.fr/static/csv/euromillions/euromillions_200402.zip",
        "https://media.fdj.fr/static/csv/euromillions/euromillions_201105.zip",
        "https://media.fdj.fr/static/csv/euromillions/euromillions_201402.zip",
        "https://media.fdj.fr/static/csv/euromillions/euromillions_201609.zip",
        "https://media.fdj.fr/static/csv/euromillions/euromillions_201902.zip",
        "https://media.fdj.fr/static/csv/euromillions/euromillions_202002.zip",
    ]

    raw_dataframes = [download_zipfile(url) for url in EUROMILLIONS_URLS]
    return format_dataframes(raw_dataframes)
