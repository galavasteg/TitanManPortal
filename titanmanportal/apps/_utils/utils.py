import datetime as dt


def get_previous_day(from_date: dt.datetime, prev_weekday: int) -> dt.datetime:
    days_delta = abs(prev_weekday - dt.datetime.now().weekday())
    prev_day = from_date - dt.timedelta(days=days_delta)
    return prev_day
