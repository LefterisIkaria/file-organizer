import logging
import shutil
import os

from src.model import Config
from src.organizer.filter_chain import *

logger = logging.getLogger(__name__)


class MoveFilesToCategoriesFilter(Filter):
    """
    Moves files from the main directory to their respective category directories.
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Moving files to their respective category directories.")
        try:
            for item in os.listdir(config.dir):
                item_path = os.path.join(config.dir, item)
                if os.path.isfile(item_path):
                    file_ext = os.path.splitext(item)[-1].lower()
                    category_name = self._determine_category(
                        file_ext, config.categories)
                    if category_name:
                        category_path = os.path.join(config.dir, category_name)
                        shutil.move(item_path, category_path)
                        logger.info(
                            f"Moved {item} to category: {category_name}")
            return chain.next(config)
        except Exception as e:
            logger.error(f"Error moving files to categories: {str(e)}")
            return FilterResponse("failure", config, str(e))

    def _determine_category(self, file_ext, categories):
        for category in categories:
            if file_ext in category.extensions:
                return category.name
        return None  # If the extension doesn't fit any category


class CategorizeByExtensionFilter(Filter):
    """
    Further categorizes files within categories based on their extensions.
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug(
            "Categorizing files within categories based on extensions.")
        try:
            for category in config.categories:
                if category.categorize_extensions:
                    category_path = os.path.join(config.dir, category.name)
                    self._categorize_files_in_directory(category_path)
            return chain.next(config)
        except Exception as e:
            logger.error(f"Error categorizing files by extensions: {str(e)}")
            return FilterResponse("failure", config, str(e))

    def _categorize_files_in_directory(self, directory_path):
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                file_ext = os.path.splitext(item)[-1].lower().lstrip(".")
                ext_dir_path = os.path.join(directory_path, file_ext)
                if not os.path.exists(ext_dir_path):
                    os.makedirs(ext_dir_path)
                    logger.info(f"Created extension directory: {ext_dir_path}")
                shutil.move(item_path, os.path.join(ext_dir_path, item))
                logger.info(
                    f"Moved {item} to extension directory: {ext_dir_path}")


class CleanupFilter(Filter):
    """
    Removes empty categories or subcategories.
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Cleaning up empty directories.")
        try:
            category_names = [
                category.name for category in config.categories] + [".Hidden", "Uncategorized"]
            for category_name in category_names:
                category_path = os.path.join(config.dir, category_name)
                self._delete_empty_directories(category_path)
            return chain.next(config)
        except Exception as e:
            logger.error(f"Error cleaning up directories: {str(e)}")
            return FilterResponse("failure", config, str(e))

    def _delete_empty_directories(self, path):
        """ Recursively delete empty directories. """
        # If directory is empty, delete it
        if not os.listdir(path):
            os.rmdir(path)
            logger.info(f"Deleted empty directory: {path}")
            return

        # Check subdirectories
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                self._delete_empty_directories(item_path)
