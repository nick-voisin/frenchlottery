import pytest

from frenchlottery.constants import LOTO_URLS
from frenchlottery.helper import LotterySource, download_zipfile
from frenchlottery.loto_helper import format_dataframe

EXPECTED_LOTO_COUNTS = {
    # "1976-2008": 4858,
    "2008-2017": 1317,
    "2017-2019": 310,
    "2019": 107,
    "2019-2026": 350,
}

@pytest.mark.parametrize("period", list(LOTO_URLS.keys()))
def test_loto_expected_counts(period: str) -> None:
    url = LOTO_URLS[period]
    expected = EXPECTED_LOTO_COUNTS[period]
    df = download_zipfile(url, source=LotterySource.LOTO)
    formatted_df = format_dataframe(df, source=LotterySource.LOTO)
    rows = formatted_df.height
    if period == "2019-2026":
        assert rows >= expected, f"URL {url} for period {period} returned {rows} rows, expected at least {expected}"
    else:
        assert rows == expected, f"URL {url} for period {period} returned {rows} rows, expected {expected}"
