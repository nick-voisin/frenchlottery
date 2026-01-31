# frenchlottery

[![CI - Test](https://github.com/nick-voisin/frenchlottery/actions/workflows/python-test.yml/badge.svg)](https://github.com/nick-voisin/frenchlottery/actions/workflows/python-test.yml) [![PyPI Latest Release](https://img.shields.io/pypi/v/frenchlottery.svg)](https://pypi.org/project/frenchlottery/) ![License](https://img.shields.io/pypi/l/frenchlottery.svg)

Simple Python package to retrieve lottery data from [FDJ](https://www.fdj.fr/) website into a Polars DataFrame.

## Installation

``pip install frenchlottery``

## Usage

### From the command line (activated env with lottery installed)

- French lottery (default) with last 5 draws:
  ``python -m frenchlottery --source=loto -n=5``
  ```
  ┌────────────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │ date       ┆ b1  ┆ b2  ┆ b3  ┆ b4  ┆ b5  ┆ e1  │
  │ ---        ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- │
  │ date       ┆ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
  ╞════════════╪═════╪═════╪═════╪═════╪═════╪═════╡
  │ 2026-01-21 ┆ 40  ┆ 25  ┆ 29  ┆ 27  ┆ 45  ┆ 10  │
  │ 2026-01-24 ┆ 30  ┆ 39  ┆ 10  ┆ 33  ┆ 18  ┆ 8   │
  │ 2026-01-26 ┆ 25  ┆ 32  ┆ 28  ┆ 9   ┆ 36  ┆ 4   │
  │ 2026-01-28 ┆ 42  ┆ 7   ┆ 11  ┆ 30  ┆ 10  ┆ 4   │
  │ 2026-01-31 ┆ 24  ┆ 14  ┆ 4   ┆ 1   ┆ 21  ┆ 4   │
  └────────────┴─────┴─────┴─────┴─────┴─────┴─────┘
  ```
- Euromillions lottery with last 10 draws:
  ``python -m frenchlottery source=euro -n=10``
  ```
  ┌────────────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │ date       ┆ b1  ┆ b2  ┆ b3  ┆ b4  ┆ b5  ┆ e1  ┆ e2  │
  │ ---        ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- │
  │ date       ┆ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
  ╞════════════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
  │ 2025-12-30 ┆ 29  ┆ 44  ┆ 26  ┆ 11  ┆ 34  ┆ 10  ┆ 1   │
  │ 2026-01-02 ┆ 46  ┆ 42  ┆ 27  ┆ 44  ┆ 8   ┆ 10  ┆ 1   │
  │ 2026-01-06 ┆ 5   ┆ 17  ┆ 18  ┆ 14  ┆ 31  ┆ 12  ┆ 10  │
  │ 2026-01-09 ┆ 10  ┆ 34  ┆ 26  ┆ 7   ┆ 1   ┆ 2   ┆ 4   │
  │ 2026-01-13 ┆ 47  ┆ 6   ┆ 44  ┆ 10  ┆ 18  ┆ 10  ┆ 2   │
  │ 2026-01-16 ┆ 5   ┆ 24  ┆ 17  ┆ 50  ┆ 29  ┆ 10  ┆ 5   │
  │ 2026-01-20 ┆ 22  ┆ 18  ┆ 19  ┆ 50  ┆ 11  ┆ 1   ┆ 11  │
  │ 2026-01-23 ┆ 4   ┆ 42  ┆ 5   ┆ 13  ┆ 21  ┆ 3   ┆ 10  │
  │ 2026-01-27 ┆ 47  ┆ 42  ┆ 23  ┆ 43  ┆ 4   ┆ 9   ┆ 3   │
  │ 2026-01-30 ┆ 14  ┆ 18  ┆ 31  ┆ 35  ┆ 46  ┆ 7   ┆ 11  │
  └────────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
  ```

### Within your project

```python
from frenchlottery import get_last_euromillions_results, get_last_loto_results

loto_res = get_last_loto_results()
euro_res = get_last_euromillions_results()
...
```

## TODO
- If `--lines` parameter is specified, no need to pull entire history. The user will most likely pull 10-15 lines.
- Add French lottery data from 1976

## NB
- This is in no way affiliated to FDJ. I'm just using it as a source of historical data.
- The initial name for the package was `lottery` which was way more elegant and worked perfectly within test PyPI (https://test.pypi.org/project/lottery/). However when publishing to PyPI, the name isn't allowed.. Great..!
