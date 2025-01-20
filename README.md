# lottery

Simple Python package to retreive lottery data from [FDJ](https://www.fdj.fr/) website.

## Installation

``pip install lottery`` (yet to come, need to upload to PyPI)

## Usage

### From the command line (activated env with lottery installed)

- French lottery:
  ``python -m lottery source=loto -n 15``
- Euromillions lottery:
  ``python -m lottery source=euro -n 5``

### Within your project

```python
from lottery import get_euromillions_results, get_loto_results

loto_res = get_loto_results()
euro_res = get_euromillions_results()
...
```