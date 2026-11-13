from collections.abc import Mapping
from datetime import datetime

import polars as pl

from frenchlottery.domain import LotterySource, get_source_urls
from frenchlottery.helper import download_zipfile, format_dataframe


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

    wrong_date_format = raw_dataframe[column_name][row_index]
    correct_date_format = datetime.strptime(wrong_date_format, from_format).strftime(to_format)
    return (
        raw_dataframe.with_row_index("__row_index")
        .with_columns(
            pl.when(pl.col("__row_index") == row_index)
            .then(pl.lit(correct_date_format))
            .otherwise(pl.col(column_name))
            .alias(column_name)
        )
        .drop("__row_index")
    )


def format_dataframes(raw_dataframes: Mapping[str, pl.DataFrame]) -> pl.DataFrame:
    """
    Applies the 'format_dataframe' function to provided list of dataframes 'raw_dataframes', and concatenates
    them into one dataframe.

    Also performs a slight cleanup of an erroneous date format in the 2014-2016 data.

    NB: Intended for internal use only.

    Args:
        raw_dataframes: Dataframes provided from zip archive extraction, keyed by period.

    Returns:
        A clean, formatted Polars DataFrame.
    """
    formatted_dfs = []
    for period, raw_dataframe in raw_dataframes.items():
        if period == "2014-2016":
            raw_dataframe = fix_datetime_format(raw_dataframe, row_index=0)

        date_format = "%Y%m%d" if period == "2004-2011" else "%d/%m/%Y"
        formatted_dfs.append(
            format_dataframe(raw_dataframe, source=LotterySource.EUROMILLIONS, date_format=date_format)
        )

    return pl.concat(formatted_dfs).sort("date")


def generate_euro_results() -> pl.DataFrame:
    """
    Gets all the historical results of the Euromillions lottery from 2004 onwards into a polars DataFrame.
    Data is downloaded from the 'Francaise des Jeux' website.

    Returns:
        pl.DataFrame: Euromillions historical results.
    """
    urls = get_source_urls(LotterySource.EUROMILLIONS)
    raw_dataframes = {
        period: download_zipfile(url, source=LotterySource.EUROMILLIONS) for period, url in urls.items()
    }
    formatted_dataframe = format_dataframes(raw_dataframes)
    return formatted_dataframe
