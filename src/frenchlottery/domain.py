from enum import Enum
from pathlib import Path

from frenchlottery.constants import EUROMILLIONS_MAPPING, EUROMILLIONS_URLS, LOTO_MAPPING, LOTO_URLS

class LotterySource(Enum):
    LOTO = "loto"
    EUROMILLIONS = "euromillions"

def get_source_from_code(source_code: str) -> LotterySource:
    match source_code.lower():
        case "loto":
            return LotterySource.LOTO
        case "euromillions" | "euro":
            return LotterySource.EUROMILLIONS
        case _:
            raise ValueError(f"Unknown source code: {source_code}")

def get_source_mapping(source: LotterySource) -> dict[str, str]:
    match source:
        case LotterySource.LOTO:
            return LOTO_MAPPING
        case LotterySource.EUROMILLIONS:
            return EUROMILLIONS_MAPPING
        case _:
            raise ValueError(f"Unknown source: {source}")

def get_source_urls(source: LotterySource) -> dict[str, str]:
    match source:
        case LotterySource.LOTO:
            return LOTO_URLS
        case LotterySource.EUROMILLIONS:
            return EUROMILLIONS_URLS
        case _:
            raise ValueError(f"Unknown source: {source}")

def get_historical_data_path(source: LotterySource) -> Path:
    data_folder = Path(__file__).parent / "data"
    match source:
        case LotterySource.LOTO:
            return data_folder / "loto_2008_2019.csv"
        case LotterySource.EUROMILLIONS:
            return data_folder / "euro_2004_2020.csv"
        case _:
            raise ValueError(f"Unknown source: {source}")