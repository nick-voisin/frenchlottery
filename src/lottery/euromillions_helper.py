from datetime import datetime

import pandas as pd

from lottery.helper import download_zipfile

# see https://www.fdj.fr/jeux-de-tirage/euromillions-my-million/historique
EUROMILLIONS_URLS = [
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afa8",
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afa9",
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afb6",
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afc6",
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afd6",
    "https://www.sto.api.fdj.fr/anonymous/service-draw-info/v3/documentations/1a2b3c4d-9876-4562-b3fc-2c963f66afe6",
]


def format_dataframe(raw_df: pd.DataFrame, date_format: str = "%d/%m/%Y") -> pd.DataFrame:
    """Formats a dataframe extracted from a Zip Archive, to the following format :
    Date | B1 | B2 | B3 | B4 | B5 | S1 | S2, where Bi represents the ball number and Si the star number.
    The returned dataframe is also indexed by date.

    Args:
        raw_df (pd.DataFrame): Raw dataframe extracted from the Zip Archive.
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

    df = raw_df.copy()
    df = df.filter(selected_columns, axis=1).rename(columns=mapper)
    df["Date"] = pd.to_datetime(df["Date"], format=date_format)
    return df.set_index("Date")


def fix_datetime_format(
    raw_dataframe: pd.DataFrame,
    row_index: int,
    column_name: str = "date_de_tirage",
    from_format: str = "%d/%m/%y",
    to_format: str = "%d/%m/%Y",
) -> pd.DataFrame:
    """
    Fixes an incorrect datetime format in 'from_format' to 'to_format' at specified row index in dataframe.
    Does not mutate original dataframe.

    Args:
        raw_dataframe: DataFrame with incorrect datetime format.
        row_index: Row at which datetime format is incorrect.
        column_name: Column where incorrect datetime format is to be found.
        from_format: Initial incorrect datetime format.
        to_format: Correct datetime format.

    Returns:
        A new dataframe with the fixed datetime format.
    """

    df = raw_dataframe.copy()
    wrong_date_format = df.at[row_index, column_name]
    correct_date_format = datetime.strptime(wrong_date_format, from_format).strftime(to_format)
    df.at[row_index, column_name] = correct_date_format

    return df


def format_dataframes(raw_dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Applies the 'format_dataframe' function to provided list of dataframes 'raw_dataframes', and concatenates
    them into one dataframe.
    Also performs a slight cleanup of an erroneous date format on the first line of the third dataframe.

    Args:
        raw_dataframes (List[pd.DataFrame]): Dataframes provided from zip archive extraction.

    Returns:
        pd.DataFrame: Clean formatted dataframe.
    """
    # Format first dataframe with date format : YYYYMMDD
    first_formatted_df = format_dataframe(raw_dataframes[0], date_format="%Y%m%d")

    # Modify date of first row of the third dataframe.
    third_fixed_df = fix_datetime_format(raw_dataframes[2], row_index=0)
    third_formatted_df = format_dataframe(third_fixed_df)

    # Format other dataframes with date format : dd/mm/yyyy
    rest_dfs = [format_dataframe(df) for idx, df in enumerate(raw_dataframes) if idx not in (0, 2)]
    formatted_dfs = [first_formatted_df, third_formatted_df]
    formatted_dfs.extend(rest_dfs)

    # concatenate along index and sort.
    concatenated_dataframe = pd.concat(formatted_dfs, axis=0)
    concatenated_dataframe.sort_index(inplace=True)

    return concatenated_dataframe


def get_euromillions_results() -> pd.DataFrame:
    """Gets all the historical results of the Euromillions lottery from 2004 onwards into a pandas DataFrame.
    Data is downloaded from the 'Francaise des Jeux' website.

    Returns:
        pd.DataFrame: Euromillions historical results.
    """

    raw_dataframes = [download_zipfile(url) for url in EUROMILLIONS_URLS]
    formatted_dataframe = format_dataframes(raw_dataframes)
    return formatted_dataframe
