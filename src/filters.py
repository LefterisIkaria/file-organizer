import os
import shutil
import logging
from config import Config
from filter_chain import *


# Get the named logger for this module
logger = logging.getLogger(__name__)


class ValidateDirectoryPathFilter(Filter):
    """
    Validates the existence of the directory path
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug(f"Validating directory path: {config.dir}")
        try:
            if not os.path.exists(config.dir):
                raise Exception(f"Directory path {config.dir} does not exist.")
            logger.info(f"Directory path {config.dir} validated successfully.")
            return chain.next(config)
        except Exception as e:
            logger.error(
                f"Error validating directory path {config.dir}: {str(e)}")
            return FilterResponse("failure", config, str(e))


class CategoryValidationCreationFilter(Filter):
    """
    Validates and creates category directories
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Validating and creating category directories.")
        try:
            for category in config.categories.keys():
                category_path = os.path.join(config.dir, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    logger.info(f"Created category directory: {category_path}")

            uncategorized_path = os.path.join(config.dir, "Uncategorized")
            if not os.path.exists(uncategorized_path):
                os.makedirs(uncategorized_path)
                logger.info(
                    f"Created 'Uncategorized' directory: {uncategorized_path}")

            return chain.next(config)
        except Exception as e:
            logger.error(
                f"Error during category validation/creation: {str(e)}")
            return FilterResponse("failure", config, str(e))


class MoveFilesToCategoryFilter(Filter):
    """
    Moves files to their respective category directories
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Moving files to their respective category directories.")
        try:
            all_files = [f for f in os.listdir(
                config.dir) if os.path.isfile(os.path.join(config.dir, f))]
            for file in all_files:
                file_moved = False
                file_ext = os.path.splitext(file)[-1].lower()
                for category, extensions in config.categories.items():
                    if file_ext in extensions:
                        shutil.move(os.path.join(config.dir, file),
                                    os.path.join(config.dir, category, file))
                        logger.info(f"Moved {file} to category: {category}")
                        file_moved = True
                        break

                if not file_moved:
                    uncategorized_path = os.path.join(
                        config.dir, "Uncategorized")
                    shutil.move(os.path.join(config.dir, file),
                                os.path.join(uncategorized_path, file))
                    logger.warning(
                        f"File {file} didn't match any category. Moved to 'Uncategorized'.")

            return chain.next(config)
        except Exception as e:
            logger.error(f"Error moving files to categories: {str(e)}")
            return FilterResponse("failure", config, str(e))


class SortByExtensionFilter(Filter):
    """
    Sorts files within categories based on extensions
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Sorting files within categories based on extensions.")
        try:
            if config.sort_extensions:
                for category in config.categories.keys():
                    category_path = os.path.join(config.dir, category)
                    all_files = [f for f in os.listdir(category_path) if os.path.isfile(
                        os.path.join(category_path, f))]
                    for file in all_files:
                        file_ext = os.path.splitext(
                            file)[-1].lower().lstrip(".")
                        ext_dir_path = os.path.join(category_path, file_ext)
                        if not os.path.exists(ext_dir_path):
                            os.makedirs(ext_dir_path)
                            logger.info(
                                f"Created extension directory: {ext_dir_path}")
                        shutil.move(os.path.join(category_path, file),
                                    os.path.join(ext_dir_path, file))
                        logger.info(
                            f"Moved {file} to extension directory: {ext_dir_path}")
            return chain.next(config)
        except Exception as e:
            logger.error(
                f"Error sorting files by extension within categories: {str(e)}")
            return FilterResponse("failure", config, str(e))
