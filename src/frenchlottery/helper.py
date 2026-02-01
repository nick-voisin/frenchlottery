
import io
from functools import cache
from zipfile import ZipFile

import polars as pl
import requests

from frenchlottery.domain import LotterySource, get_historical_data_path, get_source_mapping, get_source_urls


def read_zipfile(zip_file: ZipFile, columns: list[str] | None = None) -> pl.DataFrame:
    """
    Reads the contents of the first file in the Zip Archive 'zip_file' and converts it to a Polars DataFrame.

    Args:
        zip_file (ZipFile): Zip archive to read and extract.

    Raises:
        ValueError: No file found in zip archive.
        IOError: Unknown error during the extraction.

    Returns:
        pd.DataFrame: Content of the first file in the Zip Archive.

    """

    if not zip_file.filelist:
        raise ValueError("Cannot extract file. No file found in zip archive.")

    try:
        data = zip_file.read(name=zip_file.filelist[0].filename)
        return pl.read_csv(
            data,
            separator=";",
            columns=columns,
            encoding="latin-1",
            truncate_ragged_lines=True,
            schema_overrides={"date_de_tirage": pl.String},
        )

    except Exception as e:
        raise IOError("Could not extract data from zipfile.") from e


@cache
def request_url(url: str):
    """
    Makes an HTTP GET request to the specified URL and returns the response object.

    It caches the result of successful requests for the same URL. If the response
    status code indicates a failure (not 200), an IOError is raised with the corresponding
    status code.

    Args:
        url (str): The URL to send the GET request to.

    Raises:
        IOError: If the HTTP response code is not 200.

    Returns:
        requests.Response: The HTTP response object from the GET request.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise IOError(f"Request response returned with code {response.status_code}.")
    return response


def download_zipfile(url: str, source: LotterySource) -> pl.DataFrame:
    """
    Downloads, extracts and reads the content of the first file located in zip archive at the given url into a Polars DataFrame.

    Args:
        url (str): URL containing the Zip Archive.
        source (LotterySource): Lottery source type. Required to select proper columns.

    Raises:
        IOError: Error downloading the Zip Archive for provided url.

    Returns:
        pl.DataFrame: Content of the first file in the Zip Archive for provided url.

    """
    try:
        response = request_url(url)
        zip_file = ZipFile(io.BytesIO(response.content))
        col_mapping = get_source_mapping(source)
        return read_zipfile(zip_file, columns=list(col_mapping.keys()))
    except Exception as e:
        raise IOError(f"Unable to download data from url {url} - {e}") from e


def format_dataframe(raw_df: pl.DataFrame, source: LotterySource, date_format: str = "%d/%m/%Y") -> pl.DataFrame:
    """Formats a dataframe extracted from a zip archive using source-specific column mappings.

    The formatted dataframe contains standardized lowercase column names (date, b1, b2, ..., e1, e2, etc.)
    and is sorted by date.

    Args:
        raw_df (pl.DataFrame): Raw dataframe extracted from the zip archive.
        source (LotterySource): Lottery source type to determine the appropriate column mapping.
        date_format (str, optional): Date format for parsing. Defaults to "%d/%m/%Y".

    Returns:
        pl.DataFrame: Formatted dataframe with renamed columns and parsed date.
    """

    mapping = get_source_mapping(source)
    df = (
        raw_df.select(list(mapping.keys()))
        .rename(mapping)
        .with_columns(pl.col("date").str.strptime(pl.Date, format=date_format))
        .sort("date")
    )
    return df


def get_last_results(source: LotterySource) -> pl.DataFrame:
    """
    Returns the last results of the specified lottery source into a polars DataFrame.

    Args:
        source (LotterySource): Lottery source type.

    Returns:
        pl.DataFrame: Historical results of the specified lottery source.
    """
    urls = get_source_urls(source)
    raw_dataframe = download_zipfile(list(urls.values())[-1], source=source)
    formatted_dataframe = format_dataframe(raw_dataframe, source=source)
    return formatted_dataframe


def get_full_results(source: LotterySource) -> pl.DataFrame:
    """
    Returns the full historical results of the specified lottery source into a polars DataFrame.

    Args:
        source (LotterySource): Lottery source type.

    Returns:
        pl.DataFrame: Full historical results of the specified lottery source.
    """

    historical_data_path = get_historical_data_path(source)
    historical_data = pl.read_csv(historical_data_path, separator=",")
    live_data = get_last_results(source)
    formatted_dataframe = pl.concat([historical_data, live_data]).sort("date")
    return formatted_dataframe