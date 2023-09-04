import json
import logging

from src.filter_chain.core import FilterChain

from src.models.config import Config
from .filters import ORGANIZER_FILTERS

logger = logging.getLogger(__name__)

class FileOrganizer:

    def run(self, config_filepath: str):
        logger.info("Application started.")
        configurations = self.load_configurations(config_filepath)

        for config in configurations:
            self.process_config(config)

        logger.info("Application finished processing all configurations.")

    def load_configurations(self, filepath: str) -> list[Config]:
        try:
            with open(filepath, 'r') as f:
                conf_json = json.load(f)
                configurations = [Config(conf) for conf in conf_json]

                logger.info(f"Loaded {len(configurations)} configurations from {filepath}.")

                return configurations
        except Exception as e:
            logger.critical(f"Error loading configurations from {filepath}: {str(e)}")
            return []

    def process_config(self, config: Config):
        try:
            if not config.active:
                logger.debug(f"Skipping inactive configuration for directory: {config.dir}")
                return

            logger.info(f"Processing configuration for directory: {config.dir}")

            filters = [FilterClass() for FilterClass in ORGANIZER_FILTERS]
            chain = FilterChain(filters)
            response = chain.execute(config)

            if response.status == "success":
                logger.info(f"Successfully categorized directory: {config.dir}")
            else:
                logger.error(f"Error categorizing directory {config.dir}: {response.error}")
        except Exception as e:
            logger.error(f"Error processing configuration for directory {config.dir}: {str(e)}")