import schedule
import time
import logging

from typing import List, Dict, Any
from pipeline.base import Pipeline
from pipeline.filters import *


class Scheduler:
    SCHEDULE_MAP = {
        "hourly": lambda t: schedule.every().hour.at(t),
        "daily": lambda t: schedule.every().day.at(t),
        "weekly": lambda t: schedule.every().week.at(t),
        "interval": lambda t: schedule.every(t).minutes
    }

    def __init__(self, configs: List[Dict[str, Any]]):
        self.configs = configs

    def run_pipeline_conf(self, conf: Dict[str, Any]):
        for conf in self.configs:
            pipeline = Pipeline()
            pipeline.add_filter(ScanDirectoryFilter())
            pipeline.add_filter(FileClassificationFilter())
            pipeline.add_filter(MoveFilesFilter())

            pipeline.run(conf)
            logging.info(f"Pipeline executed for directory: {conf.get('dir')}")

    def setup(self):
        for conf in self.configs:
            schedule_info = conf.get('scheduled', {})
            frequency = schedule_info.get('frequency')
            scheduler = self.SCHEDULE_MAP.get(frequency)

            if not scheduler:
                logging.warning(
                    f"Invalid scheduling frequency: {frequency} for directory: {conf.get('dir')}")
                continue

            if frequency == "interval":
                interval_minutes = schedule_info.get("interval_minutes", 1)
                scheduler(interval_minutes).do(self.run_pipeline_conf, conf)
            else:
                scheduled_time = schedule_info.get("time", "00:00")
                scheduler(scheduled_time).do(self.run_pipeline_conf, conf)
            logging.info(
                f"Scheduled {frequency} task for directory: {conf.get('dir')} at {scheduled_time if frequency != 'interval' else str(interval_minutes) + ' minutes'}")

    def start(self):
        logging.info("Starting scheduler...")
        while True:
            schedule.run_pending()
            time.sleep(1)
