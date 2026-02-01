import pytest
from frenchlottery.constants import EUROMILLIONS_URLS
from frenchlottery.euromillions_helper import format_dataframes
from frenchlottery.helper import LotterySource, download_zipfile

EXPECTED_EURO_COUNTS = {
    "2004-2011": 378,
    "2011-2014": 286,
    "2014-2016": 276,
    "2016-2019": 253,
    "2019-2020": 97,
    "2020-": 100,  # depending on current date
}


@pytest.mark.parametrize("period", list(EUROMILLIONS_URLS.keys()))
def test_euromillions_expected_counts(period: str) -> None:
    url = EUROMILLIONS_URLS[period]
    expected = EXPECTED_EURO_COUNTS[period]
    df = download_zipfile(url, source=LotterySource.EUROMILLIONS)
    rows = df.height
    if period == "2020-":
        assert rows >= expected, f"URL {url} for period {period} returned {rows} rows, expected at least {expected}"
    else:
        assert rows == expected, f"URL {url} for period {period} returned {rows} rows, expected {expected}"


def test_can_fix_and_generate_euromillions_data_from_fdj() -> None:
    raw_dataframes = [download_zipfile(url, source=LotterySource.EUROMILLIONS) for url in EUROMILLIONS_URLS.values()]
    formatted_dataframe = format_dataframes(raw_dataframes)
    assert len(formatted_dataframe) > 0
