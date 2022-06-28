import collections
import requests
import io
import os
from typing import Optional, Union
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

# Constants
EXPORT_FILE_NAME = "euromillions.csv"


def extract_zipfile(zip_file: ZipFile, save_folder_path: Path, save_file_name: str) -> None:

    if zip_file is None:
        raise TypeError("Cannot extract file. Provided zip_file is none.")

    if not zip_file.filelist:
        raise ValueError("Cannot extract file. No file found in zip file.")

    try:
        extracted_file_name = zip_file.filelist[0].filename
        selected_path_filename = save_folder_path / save_file_name
        extracted_path_filename = save_folder_path / extracted_file_name

        if selected_path_filename.exists():
            selected_path_filename.unlink()

        zip_file.extract(extracted_file_name, save_folder_path)
        extracted_path_filename.rename(selected_path_filename)

    except Exception as e:
        print(f"Error extracting file : {extracted_file_name}.")
        raise e


def process_response(resp: requests.Response, save_folder_path: Path, save_file_name: str) -> None:
    if resp.status_code != 200:
        raise IOError(f"Request response with code {resp.status_code}.")

    try:
        zip_file = ZipFile(io.BytesIO(resp.content))
        extract_zipfile(zip_file, save_folder_path, save_file_name)
    except Exception as e:
        raise RuntimeError("Could not process response.") from e


def download_data(url: str, save_folder_path: Path, save_file_name: str) -> None:
    try:
        response = requests.get(url)
        process_response(response, save_folder_path, save_file_name)
    except Exception as e:
        raise RuntimeError(f"Unable to download data from url : {url}") from e


def valid_or_current_path(path: Optional[Union[Path, str]] = None) -> Path:
    if path is None:
        return Path(os.path.abspath(os.getcwd())) / EXPORT_FILE_NAME
    elif isinstance(path, Path):
        if not path.is_dir():
            raise OSError("Folder path does not exist.")
    elif isinstance(path, str):
        path = Path(path)
        if not path.is_dir():
            raise OSError("Folder path does not exist.")
    else:
        raise TypeError("Invalid type for provided path.")

    return path / EXPORT_FILE_NAME


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
