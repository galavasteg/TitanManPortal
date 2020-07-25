from datetime import datetime, timedelta

import utils
from periods.models import Period


def get_last_registered_period() -> Period:
    """Return last registered period"""
    last_added_period = Period.objects.latest()
    return last_added_period


def get_period_by_date(date: datetime.date) -> Period:
    """Return current period"""
    period = Period.objects.filter(
            start__lte=date, end__gte=date,
        ).first()
    return period


def get_current_period() -> Period:
    """Return current period. If there is no period in the DB,
    it will be created."""
    today = datetime.now().date()

    current_period = get_period_by_date(today)
    if not current_period:
        current_period = get_initial_period()

    return current_period


def get_initial_period(day: datetime = None) -> Period:
    day = day or datetime.now().date()
    init_period_weekday = 0

    start = utils.get_previous_day(day, init_period_weekday)
    end = start + timedelta(
            days=13, hours=23, minutes=59, seconds=59)
    init_period = Period(start=start, end=end)
    init_period.save()

    return init_period


# TODO: YAGNI 2020-07-25
# def create_new_period():
#     """Create new period after last registered one"""
#     last_Period = get_last_registered_period()
#     start = last_Period.end + timedelta(days=1)
#     end = last_Period.end + timedelta(days=14)
#
#     new_period = Period(start=start, end=end)
#     new_period.save()
#
#     return new_period
#
#
# def get_last_user_period(user: User) -> Period:
#     """Return the last period when the *user* set a goal."""
#     last_user_rating = user.rating.latest()
#     last_user_period = last_user_rating.period
#     return last_user_period
