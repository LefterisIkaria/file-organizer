from abc import ABC, abstractmethod

class Schedule(ABC):
    
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()
    
    @staticmethod
    @abstractmethod    
    def from_dict(data: dict) -> 'Schedule':
        raise NotImplementedError()

    @abstractmethod
    def _validate(self):
        raise NotImplementedError()
    

# {
#   "name": "Config3",
#   "dir": "/yet/another/directory",
#   "schedule": {
#     "time_unit": "minutes",
#     "interval": 5,
#     "day": null,
#     "time": null,
#     "active": true
#   }
# }


{
  "type": "Year",
  "interval": 1,
  "time": "14:00",
  "day": 15,
  "month": "JANUARY"
}

{
  "type": "Month",
  "interval": 3,
  "time": "20:00",
  "day": 31,
  "month": None
}

{
  "type": "Week",
  "interval": 5,
  "time": "13:30",
  "day": "Monday",
  "month": None
}

{
  "type": "Day",
  "interval": 15,
  "time": "16:30",
  "day": None,
  "month": None
}

{
  "type": "Minute",
  "interval": 40,
  "time": None,
  "day": None,
  "month": None
}

{
  "type": "Second",
  "interval": 30,
  "time": None,
  "day": None,
  "month": None
}




class DaySchedule(Schedule):

    def __init__(self, time: str = "00:00") -> None:
        self.time = time

    def to_dict(self) -> dict:
        return super().to_dict()

    @staticmethod
    def from_dict(data: dict) -> 'DaySchedule':
        return super().from_dict(data)

    def _validate(self):
        return super()._validate()
    

# other schedules