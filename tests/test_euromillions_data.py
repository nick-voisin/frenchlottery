import polars as pl
import pytest

from frenchlottery.constants import EUROMILLIONS_URLS
from frenchlottery.euromillions_helper import fix_datetime_format, format_dataframes
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
    raw_dataframes = {
        period: download_zipfile(url, source=LotterySource.EUROMILLIONS) for period, url in EUROMILLIONS_URLS.items()
    }
    formatted_dataframe = format_dataframes(raw_dataframes)
    assert len(formatted_dataframe) > 0


def _raw_dataframe(date: str) -> pl.DataFrame:
    return pl.DataFrame(
        {
            "date_de_tirage": [date],
            "boule_1": [1],
            "boule_2": [2],
            "boule_3": [3],
            "boule_4": [4],
            "boule_5": [5],
            "etoile_1": [1],
            "etoile_2": [2],
        }
    )


def test_format_dataframes_uses_period_keys_and_repairs_2014_date() -> None:
    raw_dataframes = {
        "2014-2016": _raw_dataframe("03/01/14"),
        "2011-2014": _raw_dataframe("02/01/2012"),
        "2004-2011": _raw_dataframe("20100101"),
    }

    formatted_dataframe = format_dataframes(raw_dataframes)

    assert formatted_dataframe["date"].dt.strftime("%Y-%m-%d").to_list() == [
        "2010-01-01",
        "2012-01-02",
        "2014-01-03",
    ]


def test_fix_datetime_format_does_not_mutate_input() -> None:
    raw_dataframe = _raw_dataframe("03/01/14")

    fixed_dataframe = fix_datetime_format(raw_dataframe, row_index=0)

    assert raw_dataframe["date_de_tirage"].to_list() == ["03/01/14"]
    assert fixed_dataframe["date_de_tirage"].to_list() == ["03/01/2014"]
