from pathlib import Path
import requests
import zipfile
import io

def remove_csv_files(folder_path: Path) -> None:
    for file_path in folder_path.glob('*.csv'):
        file_path.unlink()


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