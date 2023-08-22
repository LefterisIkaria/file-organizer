import json
import logging

from typing import Dict, Any, List
from logger_config import LoggerConfig
from scheduler import Scheduler


def main():
    logger_config = LoggerConfig()
    logger_config.setup_file_logging()

    configs = load_configs('config.json')
    scheduler = Scheduler(configs)
    scheduler.setup()
    scheduler.start()


def load_configs(filename: str) -> List[Dict[str, Any]]:
    try:
        with open(filename, 'r') as file:
            configs = json.load(file)

        logging.info(f"Loaded {len(configs)} configurations from {filename}")
        return configs
    except Exception as e:
        logging.error(f"Error loading configurations: {e}")
        return []


if __name__ == "__main__":
    main()
