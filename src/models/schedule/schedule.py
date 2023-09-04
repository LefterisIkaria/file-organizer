import re
from .schedule_enums import Day, Month, ScheduleType


class Schedule:
    
    def __init__(
            self, 
            type: ScheduleType,
            interval: int = 1,
            time: str = None,
            day: Day = None,
            month: Month = None,
            date: int = None,
            active: bool = False

    ) -> None:        
        self.type = type
        self.interval = interval
        self.time = time
        self.day = day
        self.month = month
        self.date = date
        self.active = active

        self._validate()
    
    def to_dict(self) -> dict:
        return {
            'type': self.type.name,
            'interval': self.interval,
            'time': self.time,
            'day': self.day.name,
            'month': self.month.name,
            'date': self.date,
            'active': self.active
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Schedule':
        return Schedule(
            ScheduleType.from_str_value(data.get("type")),
            data.get('interval'),
            data.get('time'),
            Day.from_str_value(data.get('day')),
            Month.from_str_value(data.get('month')),
            data.get('date'),
            data.get('active')
        )
    
    
    def _validate(self):
        if self.interval < 0:
            raise ValueError("Invalid value: interval must be greater than 0")
        
        type_validators = {
            ScheduleType.DAY: self._validate_day,
            ScheduleType.WEEK: self._validate_week,
            ScheduleType.MONTH: self._validate_month,
            ScheduleType.YEAR: self._validate_year,
        }
        
        validator = type_validators.get(self.type)
        if validator:
            validator()
    
    def _validate_day(self):
        if not Schedule.validate_time(self.time):
            raise ValueError("Invalid time format or range")
    
    def _validate_week(self):
        self._validate_day()
    
    def _validate_month(self):
        self._validate_day()
        if self.date < 1 or self.date > 31:
            raise ValueError("Invalid date, is out of range [1, 31]")
    
    def _validate_year(self):
        self._validate_month()
    

    @staticmethod
    def validate_time(time: str) -> bool:
        # Validate the format using regular expression
        if not re.match(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$', time):
            return False
        return True
        
