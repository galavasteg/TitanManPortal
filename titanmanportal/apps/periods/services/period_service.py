from datetime import datetime, timedelta

from ..models import Period


class PeriodService:

    PERIOD_MODEL = Period

    @staticmethod
    def get_last_registered_period() -> Period:
        """Return last registered period"""
        last_added_period = Period.objects.latest()
        return last_added_period

    @staticmethod
    def get_period_by_date(date: datetime.date) -> Period:
        """Return current period"""
        period = Period.objects.filter(
                start__gte=date, end__lte=date,
            ).first()
        return period

    @classmethod
    def get_current_period(cls) -> Period:
        """Return current period"""
        today = datetime.now().date()
        current_period = cls.get_period_by_date(today)
        return current_period

    @classmethod
    def create_new_period(cls):
        """Create new period after last registered one"""
        last_Period = cls.get_last_registered_period()
        start = last_Period.end + timedelta(days=1)
        end = last_Period.end + timedelta(days=14)
        new_period = Period(start=start, end=end)
        new_period.save()

