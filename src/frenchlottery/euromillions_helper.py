from datetime import datetime

import polars as pl
from frenchlottery.domain import get_source_urls
from frenchlottery.helper import LotterySource, download_zipfile, format_dataframe


def fix_datetime_format(
    raw_dataframe: pl.DataFrame,
    row_index: int,
    column_name: str = "date_de_tirage",
    from_format: str = "%d/%m/%y",
    to_format: str = "%d/%m/%Y",
) -> pl.DataFrame:
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

    col_vals = raw_dataframe[column_name].to_list()
    wrong_date_format = col_vals[row_index]
    correct_date_format = datetime.strptime(wrong_date_format, from_format).strftime(to_format)
    col_vals[row_index] = correct_date_format
    df = raw_dataframe.with_columns(pl.Series(column_name, col_vals))
    return df


def format_dataframes(raw_dataframes: list[pl.DataFrame]) -> pl.DataFrame:
    """
    Applies the 'format_dataframe' function to provided list of dataframes 'raw_dataframes', and concatenates
    them into one dataframe.

    Also performs a slight cleanup of an erroneous date format on the first line of the third dataframe (2014-2016).

    NB: Intended for internal use only.

    Args:
        raw_dataframes (List[pd.DataFrame]): Dataframes provided from zip archive extraction.

    Returns:
        pd.DataFrame: Clean formatted dataframe.
    """
    # Format first dataframe with date format : YYYYMMDD
    first_formatted_df = format_dataframe(raw_dataframes[0], source=LotterySource.EUROMILLIONS, date_format="%Y%m%d")

    # Modify date of first row of the third dataframe.
    third_fixed_df = fix_datetime_format(raw_dataframes[2], row_index=0)
    third_formatted_df = format_dataframe(third_fixed_df, source=LotterySource.EUROMILLIONS)

    # Format other dataframes with date format : dd/mm/yyyy
    rest_dfs = [
        format_dataframe(df, source=LotterySource.EUROMILLIONS)
        for idx, df in enumerate(raw_dataframes)
        if idx not in (0, 2)
    ]
    formatted_dfs = [first_formatted_df, third_formatted_df]
    formatted_dfs.extend(rest_dfs)

    # concatenate along Date and sort.
    concatenated_dataframe = pl.concat(formatted_dfs)
    concatenated_dataframe = concatenated_dataframe.sort("date")

    return concatenated_dataframe


def generate_results() -> pl.DataFrame:
    """
    Gets all the historical results of the Euromillions lottery from 2004 onwards into a polars DataFrame.
    Data is downloaded from the 'Francaise des Jeux' website.

    Returns:
        pl.DataFrame: Euromillions historical results.
    """
    urls = get_source_urls(LotterySource.EUROMILLIONS)
    raw_dataframes = [download_zipfile(url, source=LotterySource.EUROMILLIONS) for url in urls.values()]
    formatted_dataframe = format_dataframes(raw_dataframes)
    return formatted_dataframe
