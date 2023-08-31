import json
import logging

from typing import List

from src.model import Config
from src.organizer.filters.filter_chain_constructor import build_filter_chain

logger = logging.getLogger(__name__)

class FileOrganizer:

    def run(self, config_filepath: str):
        logger.info("Application started.")
        configurations = self.load_configurations(config_filepath)

        for config in configurations:
            self.process_config(config)

        logger.info("Application finished processing all configurations.")

    def load_configurations(self, filepath: str) -> List[Config]:
        try:
            with open(filepath, 'r') as f:
                conf_json = json.load(f)
                configurations = [Config(conf) for conf in conf_json]

                logger.info(
                    f"Loaded {len(configurations)} configurations from config.json.")

                return configurations
        except Exception as e:
            logger.critical(
                f"Error loading configurations from config.json: {str(e)}")
            return []

    def process_config(self, config: Config):
        try:
            if not config.active:
                logger.debug(
                    f"Skipping inactive configuration for directory: {config.dir}")
                return

            logger.info(
                f"Processing configuration for directory: {config.dir}")

            chain = build_filter_chain()
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