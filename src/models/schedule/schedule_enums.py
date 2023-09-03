import calendar
from enum import Enum, StrEnum, auto


class ScheduleEnum(Enum):

    @classmethod
    def from_str_value(cls, value: str):
        return cls[value.upper()] if value else None
    


class ScheduleType(ScheduleEnum):
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4
    WEEK = 5
    MONTH = 6
    YEAR = 7


class Day(ScheduleEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Month(ScheduleEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


    def days(self, year: int) -> int:
        return calendar.monthrange(year, self.value)[1]
