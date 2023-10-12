import datetime as dt

from constants import DATE_FORMAT_PATTERN


class DateTimeWorker:
    """Helper class for working with datetime."""

    @staticmethod
    def get_timedelta(delta_days: int) -> dt.timedelta:
        return dt.timedelta(delta_days)

    @staticmethod
    def get_current_date() -> dt.datetime:
        return dt.datetime.now()

    @staticmethod
    def create_date(
        date_str: str,
        format: str = DATE_FORMAT_PATTERN
    ) -> dt.datetime:
        return dt.datetime.strptime(date_str, format)
