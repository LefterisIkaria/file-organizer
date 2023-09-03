import logging
import shutil
import os

from src.models.config import Config
from src.filter_chain.core import *

logger = logging.getLogger(__name__)


class CategoryExistenceFilter(Filter):
    """
    Ensures that each category directory exists. If not, it creates it.
    """

    priority: int = 2

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Ensuring category directories exist.")
        try:
            # Create Uncategorized directory if not exists
            uncategorized_path = os.path.join(config.dir, "Uncategorized")
            if not os.path.exists(uncategorized_path):
                os.mkdir(uncategorized_path)

            # Create other categories if they not exists
            for category in config.categories:
                category_path = os.path.join(config.dir, category.name)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    logger.info(f"Created category directory: {category_path}")
            return chain.next(config)
        except Exception as e:
            logger.error(
                f"Error ensuring category directory existence: {str(e)}")
            return FilterResponse("failure", config, str(e))


class CategoryExtensionSubdirsValidationFilter(Filter):
    """
    Validates the existence or absence of extension subdirectories based on the 
    categorize_extensions flag of each category.
    """

    priority: int = 3

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug(
            "Handling extension subdirectories based on category flags.")
        try:
            for category in config.categories:
                category_path = os.path.join(config.dir, category.name)
                if category.categorize_extensions:
                    self._validate_or_create_ext_subdirs(
                        category_path, category.extensions)
                else:
                    self._validate_and_cleanup_ext_subdirs(category_path)
            return chain.next(config)
        except Exception as e:
            logger.error(
                f"Error validating extension subdirectories: {str(e)}")
            return FilterResponse("failure", config, str(e))

    def _validate_or_create_ext_subdirs(self, category_path, extensions):
        for ext in extensions:
            ext_dir = os.path.join(category_path, ext.lstrip("."))
            if not os.path.exists(ext_dir):
                os.makedirs(ext_dir)
                logger.info(f"Created extension subdirectory: {ext_dir}")

    def _validate_and_cleanup_ext_subdirs(self, category_path):
        for item in os.listdir(category_path):
            item_path = os.path.join(category_path, item)
            if os.path.isdir(item_path):  # if it's a subdirectory
                # Move files from subdirectory to main category directory
                for file in os.listdir(item_path):
                    shutil.move(os.path.join(item_path, file), category_path)
                os.rmdir(item_path)
                logger.info(f"Removed extension subdirectory: {item_path}")
