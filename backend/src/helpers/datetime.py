import datetime as dt
from typing import Any, Union

from core.constants import (
    DATE_FORMAT_PATTERN,
    HOUR_EXPIRE,
    HOURS_PER_DAY,
    MINUTE_EXPIRE,
    SECONDS_PER_DAY
)


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

    @staticmethod
    def datetime_parser(data: dict) -> dict:
        for k, v in data.items():
            if isinstance(v, str) and v.endswith('00:00'):
                try:
                    data[k] = dt.datetime.fromisoformat(v)
                except Exception:
                    pass

        return data

    @staticmethod
    def serialize_dates(value: Any) -> Union[Any, str]:
        return value.isoformat() if isinstance(value, dt.datetime) else value

    @staticmethod
    def get_seconds_left(
        hour: int = HOUR_EXPIRE,
        minute: int = MINUTE_EXPIRE
    ) -> int:
        """
        Takes hours and minutes and
        returns the number of seconds until that time.
        """
        now: dt.datetime = dt.datetime.now()
        return int(
            (
                dt.timedelta(hours=HOURS_PER_DAY)
                - (
                    now - now.replace(
                        hour=hour,
                        minute=minute,
                        second=0,
                        microsecond=0
                    )
                )
            )
            .total_seconds() % SECONDS_PER_DAY
        )
