import io
from functools import cache
from zipfile import ZipFile

import pandas as pd
import requests


def read_zipfile(zip_file: ZipFile) -> pd.DataFrame:
    """
    Reads the contents of the first file in the Zip Archive 'zip_file' and converts it to a Pandas DataFrame.

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
        text_raw = data.decode("latin-1")
        return pd.read_csv(io.StringIO(text_raw), sep=";", index_col=False)

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


def download_zipfile(url: str) -> pd.DataFrame:
    """
    Downloads, extracts and reads the content of the first file located in zip archive at the given url
    into a Pandas DataFrame.

    Args:
        url (str): URL containing the Zip Archive.

    Raises:
        IOError: Error downloading the Zip Archive for provided url.

    Returns:
        pd.DataFrame: Content of the first file in the Zip Archive for provided url.

    """
    try:
        response = request_url(url)
        zip_file = ZipFile(io.BytesIO(response.content))
        return read_zipfile(zip_file)
    except Exception as e:
        raise IOError(f"Unable to download data from url : {url}") from e
