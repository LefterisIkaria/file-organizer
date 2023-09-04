import schedule
import time
import logging

from models.schedule.schedule import *
from models.schedule.schedule_enums import ScheduleType

logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, time_schedule: Schedule):
        self.time_schedule = time_schedule

    def get_job(self) -> schedule.Job:
        if  self.time_schedule.type == ScheduleType.SECOND:
            return schedule.every(self.time_schedule.interval).seconds
        elif self.time_schedule.type == ScheduleType.MINUTE:
            return schedule.every(self.time_schedule.interval).minutes
        elif self.time_schedule.type == ScheduleType.HOUR:
            return schedule.every(self.time_schedule.interval).hours
        elif self.time_schedule.type == ScheduleType.DAY:
            return schedule.every(self.time_schedule.interval).days.at(self.time_schedule.specific_time)
        elif self.time_schedule.type == ScheduleType.WEEK:
            return schedule.every(self.time_schedule.interval).weeks
        elif self.time_schedule.type == ScheduleType.MONTH:
            # Monthly scheduling 
            pass
        elif self.time_schedule.type == ScheduleType.YEAR:
            # Yearly scheduling
            pass

    def run_task(self, task, *args, **kwargs):
        if self.time_schedule.active:
            if task:
                logger.debug(f"Running job for {self.time_schedule.type}")
                self.get_job().do(task, *args, **kwargs)
        else:
            logger.warning(f"Skipping task for {self.time_schedule.type} as it is not active.")

    def start(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

