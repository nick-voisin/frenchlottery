import pytest

from lottery.helper import download_zipfile
from lottery.loto_helper import LOTO_URLS, format_dataframes


@pytest.mark.parametrize("url", LOTO_URLS)
def test_can_read_loto_data_from_fdj(url: str) -> None:
    raw_dataframe = download_zipfile(url)
    assert len(raw_dataframe) > 0


def test_can_format_loto_data_from_fdj() -> None:
    raw_dataframes = [download_zipfile(url) for url in LOTO_URLS]
    formatted_dataframe = format_dataframes(raw_dataframes)
    assert len(formatted_dataframe) > 0
