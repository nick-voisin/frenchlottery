import collections
import requests
import zipfile
import io
from pathlib import Path
import pandas as pd


def download_zipped_file(url: str) -> zipfile.ZipFile:
    response = requests.get(url)
    if response.status_code == 200:
        return zipfile.ZipFile(io.BytesIO(response.content))
    else:
        raise Exception(f"Could not read from url: {url}")


def save_zipped_file(zip_file: zipfile.ZipFile, save_folder_path: Path, save_file_name: str) -> None:
    extracted_file_name = zip_file.filelist[0].filename

    selected_path_filename = save_folder_path / save_file_name
    extracted_path_filename = save_folder_path / extracted_file_name

    if selected_path_filename.exists():
        selected_path_filename.unlink()

    zip_file.extract(extracted_file_name, save_folder_path)
    extracted_path_filename.rename(selected_path_filename)


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
