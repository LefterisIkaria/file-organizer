import json
import logging
from src.models.config_manager import ConfigManager
from src.filter_chain.core import FilterChain
from src.models.config import Config

from .filters import ORGANIZER_FILTERS

logger = logging.getLogger(__name__)

class FileOrganizer:

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.configurations = self.config_manager.get_configs()


    def process_all(self):
        logger.info("Application started running all configurations.")

        for config in self.configurations:
            if not config.active:
                logger.debug(f"Skipping inactive configuration for directory: {config.dir}")
                continue
            
            self.process_config(config)

        logger.info("Application finished processing all configurations.")


    def process_config(self, config: Config):
        try:
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