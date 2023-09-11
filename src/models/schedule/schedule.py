from src.models.schedule.schedule_enums import Month, ScheduleType, WeekDay


class Schedule:
    
    def __init__(self, type: ScheduleType, interval: int = 1, time: str = None, weekday: WeekDay = None, month: Month = None, day: int = None, active: bool = False) -> None: 
        self.type = type
        self.interval = interval
        self.time = time
        self.weekday = weekday
        self.month = month
        self.day = day
        self.active = active

    
    def to_dict(self) -> dict:
        return {
            'type': self.type.name,
            'interval': self.interval,
            'time': self.time if self.time else None,
            'weekday': self.weekday.name if self.weekday else None,
            'month': self.month.name if self.month else None,
            'day': self.day if self.day else None,
            'active': self.active
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Schedule':
        return Schedule(
            type=ScheduleType.from_str_value(data.get("type")),
            interval=data.get('interval'),
            time=data.get('time'),
            weekday=WeekDay.from_str_value(data.get('weekday')),
            month=Month.from_str_value(data.get('month')),
            day=data.get('day'),
            active=data.get('active')
        )
    
    def __str__(self) -> str:

        
        base_str = ""
        if self.interval == 1:
            base_str += f"Every {self.type.name.capitalize()}"
        else:
           base_str += f"Every {self.interval} {self.type.name.capitalize()}s"

        if self.month:
            base_str += f", In: {self.month.name.capitalize()}"
        
        if self.day:
            base_str += f", {self.day}"

        if self.weekday:
            base_str += f", On: {self.weekday.name.capitalize()}"
        
        if self.time:
            base_str += f", At: {self.time}"

        return base_str