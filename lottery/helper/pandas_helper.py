import collections

import pandas as pd


def loop(df: pd.DataFrame):
    """
    Creates a generator to iterate over a Pandas DataFrame : yields a named tuple for each row.
    Tuple properties are based on provided DataFrame columns.

    Parameters
    ----------
    df : pd.DataFrame

    Yields
    -------
    Generator[Tuple]
    """
    col_names_concat = [col_name for col_name in list(df.columns)]
    col_names_concat.insert(0, "Date")
    Row = collections.namedtuple("Row", col_names_concat)
    for row in df.itertuples():
        yield Row(*row)