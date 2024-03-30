import pandas as pd

from lottery.helper import download_zipfile


def format_dataframe(raw_df: pd.DataFrame, date_format: str = "%d/%m/%Y") -> pd.DataFrame:
    """Formats a dataframe extracted from a Zip Archive, to the following format :
    Date | B1 | B2 | B3 | B4 | B5 | S1, where Bi represents the ball number and Si the star number.
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
        "numero_chance",
    ]
    renamed_columns = ["Date", "B1", "B2", "B3", "B4", "B5", "S1"]
    mapper = dict(zip(selected_columns, renamed_columns))

    df = raw_df.copy()
    df = df[selected_columns]
    df = df.rename(columns=mapper)
    df.loc[:, "Date"] = pd.to_datetime(df.loc[:, "Date"], format=date_format)
    df.set_index("Date", inplace=True)
    return df

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
    Gets all the historical results of the french lottery from 2004 onwards into a pandas DataFrame.
    Data is downloaded from the 'Francaise des Jeux' website.

    Returns:
        pd.DataFrame: Loto historical results.
    """

    EUROMILLIONS_URLS = [
        "https://media.fdj.fr/static-draws/csv/loto/loto_200810.zip",
        "https://media.fdj.fr/static-draws/csv/loto/loto_201703.zip",
        "https://media.fdj.fr/static-draws/csv/loto/loto_201902.zip",
        "https://media.fdj.fr/static-draws/csv/loto/loto_201911.zip",
    ]

    raw_dataframes = [download_zipfile(url) for url in EUROMILLIONS_URLS]
    formatted_dataframe = format_dataframes(raw_dataframes)
    return formatted_dataframe