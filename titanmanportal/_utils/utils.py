import datetime as dt
from pathlib import Path
from typing import Optional


def get_previous_day(from_date: dt.datetime, prev_weekday: int) -> dt.datetime:
    days_delta = abs(prev_weekday - dt.datetime.now().weekday())
    prev_day = from_date - dt.timedelta(days=days_delta)
    return prev_day


def try_load_dotenv(path: Optional[Path] = None):
    try:
        from dotenv import load_dotenv
        load_dotenv(path)
    except ImportError:
        pass
