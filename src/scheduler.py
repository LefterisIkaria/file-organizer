import schedule
import time
import logging

from typing import List, Dict, Any


class Scheduler:
    SCHEDULE_MAP = {
        "hourly": lambda t: schedule.every().hour.at(t),
        "daily": lambda t: schedule.every().day.at(t),
        "weekly": lambda t: schedule.every().week.at(t),
        "interval": lambda t: schedule.every(t).minutes
    }
