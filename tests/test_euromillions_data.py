import pytest

from lottery.euromillions_helper import EUROMILLIONS_URLS, format_dataframes
from lottery.helper import download_zipfile


@pytest.mark.parametrize("url", EUROMILLIONS_URLS)
def test_can_read_euromillions_data_from_fdj(url: str) -> None:
    raw_dataframe = download_zipfile(url)
    assert len(raw_dataframe) > 0


def test_can_fix_euromillions_data_from_fdj() -> None:
    raw_dataframes = [download_zipfile(url) for url in EUROMILLIONS_URLS]
    formatted_dataframe = format_dataframes(raw_dataframes)
    assert len(formatted_dataframe) > 0



