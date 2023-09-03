import logging
import shutil
import os

from src.models.config import Config
from src.filter_chain.core import *

logger = logging.getLogger(__name__)


class FileHiddenFilter(Filter):
    """
    Handles hidden files by moving them to a "Hidden" directory.
    """

    priority: int = 4

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Checking for hidden files.")
        try:
            hidden_dir_path = os.path.join(config.dir, ".Hidden")
            if not os.path.exists(hidden_dir_path):
                os.makedirs(hidden_dir_path)
                logger.info(f"Created '.Hidden' directory: {hidden_dir_path}")

            # Iterate over all categories, including "Uncategorized"
            categories = [
                category.name for category in config.categories] + ["Uncategorized"]
            for category in categories:
                category_path = os.path.join(config.dir, category)
                for item in os.listdir(category_path):
                    if item.startswith('.'):
                        # Move the hidden file to the "Hidden" directory
                        shutil.move(os.path.join(
                            category_path, item), hidden_dir_path)
                        logger.info(
                            f"Moved hidden file {item} to '.Hidden' directory.")

            return chain.next(config)
        except Exception as e:
            logger.error(f"Error handling hidden files: {str(e)}")
            return FilterResponse("failure", config, str(e))


class FileValidationFilter(Filter):
    """
    Validates that files are correctly placed based on their extensions.
    """

    priority: int = 5

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Validating file placements based on extensions.")
        try:
            for category in config.categories:
                category_path = os.path.join(config.dir, category.name)
                self._validate_files_in_category(
                    config.dir, category, category_path)
            return chain.next(config)
        except Exception as e:
            logger.error(f"Error validating file placements: {str(e)}")
            return FilterResponse("failure", config, str(e))

    def _validate_files_in_category(self, dir, category, category_path):
        for item in os.listdir(category_path):
            item_path = os.path.join(category_path, item)
            if os.path.isfile(item_path):
                file_ext = os.path.splitext(item)[-1].lower()
                if file_ext not in category.extensions:
                    # Move the file back to the main directory
                    shutil.move(item_path, dir)
                    logger.warning(
                        f"Moved {item} back to main directory as it didn't match category extensions.")


class FileExtensionFilter(Filter):
    """
    Handles files without extensions or with unusual extensions.
    """

    priority: int = 6

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Checking for files without or with unusual extensions.")
        try:
            uncategorized_path = os.path.join(config.dir, "Uncategorized")
            for item in os.listdir(config.dir):
                item_path = os.path.join(config.dir, item)
                if os.path.isfile(item_path):
                    file_ext = os.path.splitext(item)[-1].lower()
                    # If the file doesn't have an extension or doesn't fit any category
                    if not file_ext or not self._fits_any_category(file_ext, config.categories):
                        shutil.move(item_path, uncategorized_path)
                        logger.warning(
                            f"Moved {item} to 'Uncategorized' as it doesn't have an extension or didn't fit any category.")
            return chain.next(config)
        except Exception as e:
            logger.error(f"Error handling files without extensions: {str(e)}")
            return FilterResponse("failure", config, str(e))

    def _fits_any_category(self, file_ext, categories):
        for category in categories:
            if file_ext in category.extensions:
                return True
        return False
