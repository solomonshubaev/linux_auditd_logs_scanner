import logging
from abc import ABC
from datetime import datetime
from typing import Optional

UNIX_FORMAT = "%Y-%m-%d %H:%M:%S"


class DatetimeUtils(ABC):

    @staticmethod
    def datetime_to_str(date: datetime, *, format_str: str = UNIX_FORMAT) -> Optional[str]:
        try:
            return date.strftime(format_str)
        except ValueError as e:
            logging.warning(f"Couldn't convert datetime to str. {date=}, error message: {str(e)}")
            return None

    @staticmethod
    def str_to_datetime(date_string: str, *, format_str: str = UNIX_FORMAT) -> Optional[datetime]:
        try:
            return datetime.strptime(date_string, format_str)
        except ValueError as e:
            logging.warning(f"Couldn't convert str to datetime. {date_string=}, error message: {str(e)}")
            return None

    @staticmethod
    def str_timestamp_to_datetime(date_string: str) -> Optional[datetime]:
        try:
            return datetime.fromtimestamp(float(date_string))
        except ValueError as e:
            logging.warning(f"Couldn't convert str to datetime. {date_string=}, error message: {str(e)}")
            return None

    @staticmethod
    def datetime_now(datetime_zone=None) -> datetime:
        return datetime.now(datetime_zone)
