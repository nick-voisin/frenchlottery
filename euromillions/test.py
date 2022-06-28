import os
from datetime import datetime
from typing import List, Any, Optional
from dataclasses import dataclass, field

import pandas as pd
from pathlib import Path
import zipfile
import io
from euromillions.helper import download_data, loop, request_data, process_response
#%%
EUROMILLIONS_ORIGINAL_PATH = Path("C:\Dev\Python\lottery\euromillions\data\original")
EUROMILLIONS_FORMATTED_PATH = Path("C:\Dev\Python\lottery\euromillions\data\formateed")
EUROMILLIONS_URLS = [
    "https://media.fdj.fr/static/csv/euromillions/euromillions_200402.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_201105.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_201402.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_201609.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_201902.zip",
    "https://media.fdj.fr/static/csv/euromillions/euromillions_202002.zip",
]

data = request_data(EUROMILLIONS_URLS[0])
save_file_name = "file_test.csv"
resp = process_response(data, EUROMILLIONS_ORIGINAL_PATH, save_file_name)

zip_file = zipfile.ZipFile(io.BytesIO(data.content))
extracted_file_name = zip_file.filelist[0].filename
selected_path_filename = EUROMILLIONS_ORIGINAL_PATH / save_file_name
extracted_path_filename = EUROMILLIONS_ORIGINAL_PATH / extracted_file_name

if selected_path_filename.exists():
    selected_path_filename.unlink()

zip_file.extract(extracted_file_name, EUROMILLIONS_ORIGINAL_PATH)
extracted_path_filename.rename(selected_path_filename)