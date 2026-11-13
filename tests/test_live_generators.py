import pytest

from frenchlottery.euromillions_helper import generate_euro_results
from frenchlottery.loto_helper import generate_loto_results

# Set to True when running these live FDJ integration tests locally.
RUN_LIVE_INTEGRATION_TESTS = False


@pytest.mark.skipif(
    not RUN_LIVE_INTEGRATION_TESTS,
    reason="Live FDJ integration tests are disabled; set RUN_LIVE_INTEGRATION_TESTS to True to run them.",
)
def test_generate_euro_results_live() -> None:
    results = generate_euro_results()

    assert results.height > 0
    assert {"date", "b1", "b2", "b3", "b4", "b5", "e1"}.issubset(results.columns)
    assert results["date"].is_sorted()


@pytest.mark.skipif(
    not RUN_LIVE_INTEGRATION_TESTS,
    reason="Live FDJ integration tests are disabled; set RUN_LIVE_INTEGRATION_TESTS to True to run them.",
)
def test_generate_loto_results_live() -> None:
    results = generate_loto_results()

    assert results.height > 0
    assert {"date", "b1", "b2", "b3", "b4", "b5", "e1"}.issubset(results.columns)
    assert results["date"].is_sorted()
