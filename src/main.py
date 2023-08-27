import json
import logging

from logging.handlers import RotatingFileHandler
from filter_chain import FilterChain
from filters import *


def main():
    file_organizer = FileOrganizer()
    file_organizer.run()


class FileOrganizer:
    def __init__(self, log_level=logging.INFO) -> None:
        self.logger = self.set_up_file_logging(log_level=logging.DEBUG)

    def run(self):
        self.logger.info("Application started.")
        configurations = self.load_configurations("config.json")

        for config in configurations:
            self.process_config(config)

        self.logger.info("Application finished processing all configurations.")

    def setup_file_logging(self, filename='app.log', log_level=logging.INFO, max_log_size=5*1024*1024, backup_count=3):
        """
        Setup file logging.

        Parameters:
        - filename: Name of the log file.
        - log_level: Logging level (e.g., logging.DEBUG, logging.INFO).
        - max_log_size: Maximum log file size (in bytes) before it gets rotated.
        - backup_count: Number of backup log files to keep.
        """

        logger = logging.getLogger()

        # Check if handlers are already added to avoid duplicate logs
        if not logger.handlers:
            logger.setLevel(log_level)

            # File handler with rotation
            file_handler = RotatingFileHandler(
                filename, maxBytes=max_log_size, backupCount=backup_count)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # Optional: Stream handler to see logs in console (useful for debugging)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(file_formatter)
            logger.addHandler(stream_handler)

        return logger

    def load_configurations(self, file_path: str) -> List[Config]:
        try:
            with open("config.json", 'r') as f:
                configurations = json.load(f)
                logger.info(
                    f"Loaded {len(configurations)} configurations from config.json.")

                return configurations
        except Exception as e:
            logger.critical(
                f"Error loading configurations from config.json: {str(e)}")
            return []

    def proccess_config(self, config: Config):
        try:
            if not config.active:
                logger.debug(
                    f"Skipping inactive configuration for directory: {config.dir}")
                return

            logger.info(
                f"Processing configuration for directory: {config.dir}")

            filters = [
                ValidateDirectoryPathFilter(),
                CategoryValidationCreationFilter(),
                MoveFilesToCategoryFilter(),
                SortByExtensionFilter()
            ]

            chain = FilterChain(filters)
            response = chain.execute(config)

            if response.status == "success":
                logger.info(
                    f"Successfully categorized directory: {config.dir}")
            else:
                logger.error(
                    f"Error categorizing directory {config.dir}: {response.error}")
        except Exception as e:
            logger.error(
                f"Error processing configuration for directory {config.dir}: {str(e)}")


if __name__ == "__main__":
    main()
