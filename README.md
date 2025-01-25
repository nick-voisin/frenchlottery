# frenchlottery

[![CI - Test](https://github.com/nick-voisin/frenchlottery/actions/workflows/python-test.yml/badge.svg)](https://github.com/nick-voisin/frenchlottery/actions/workflows/python-test.yml) [![PyPI Latest Release](https://img.shields.io/pypi/v/frenchlottery.svg)](https://pypi.org/project/frenchlottery/) ![License](https://img.shields.io/pypi/l/frenchlottery.svg)

Simple Python package to retrieve lottery data from [FDJ](https://www.fdj.fr/) website.

## Installation

``pip install frenchlottery``

## Usage

### From the command line (activated env with lottery installed)

- French lottery (default) with last 15 draws:
  ``python -m frenchlottery -n 15``
- Euromillions lottery with last 5 draws:
  ``python -m frenchlottery source=euro -n 5``

### Within your project

```python
from frenchlottery import get_euromillions_results, get_loto_results

loto_res = get_loto_results()
euro_res = get_euromillions_results()
...
```

## TODO
- If `--lines` parameter is specified, no need to pull entire history. The user will most likely pull 10-15 lines.

## NB
- This is in no way affiliated to FDJ. I'm just using it as a source of historical data.
- The initial name for the package was `lottery` which was way more elegant and worked perfectly within test PyPI (https://test.pypi.org/project/lottery/). However when publishing to PyPI, the name isn't allowed.. Great..!
