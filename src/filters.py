import os
import shutil
import logging
from model import Config
from filter_chain import *


# Get the named logger for this module
logger = logging.getLogger(__name__)


class ValidateDirectoryPathFilter(Filter):
    """
    Validates the existence of the directory path.
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
    Validates and creates category directories.
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Validating and creating category directories.")
        try:
            for category in config.categories:
                category_path = os.path.join(config.dir, category.name)

                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    logger.info(f"Created category directory: {category_path}")

                # If category has categorize_extentions set to True
                if category.categorize_extentions:
                    self._validate_extention_subdirs(
                        category_path, category.extentions)
                else:
                    self._clean_extention_subdirs(category_path)

            return chain.next(config)
        except Exception as e:
            logger.error(
                f"Error during category validation/creation: {str(e)}")
            return FilterResponse("failure", config, str(e))

    def _validate_extention_subdirs(self, category_path: str, extensions: List[str]):
        # Ensure the required extension subdirectories exist
        for ext in extensions:
            ext_dir = os.path.join(category_path, ext.lstrip("."))
            if not os.path.exists(ext_dir):
                os.makedirs(ext_dir)
                logger.info(f"Created extension directory: {ext_dir}")

            # Check if the files inside the extension dir match the expected extension
            for file in os.listdir(ext_dir):
                file_ext = os.path.splitext(file)[-1].lower()
                if file_ext != ext:
                    # Move the file back to the main category directory
                    shutil.move(os.path.join(ext_dir, file), category_path)
                    logger.warning(
                        f"Moved {file} out of {ext_dir} due to mismatched extension.")

    def _clean_extention_subdirs(self, category_path: str):
        # Move files out from any extension subdirectories and delete the subdirectories
        for subdir in os.listdir(category_path):
            subdir_path = os.path.join(category_path, subdir)
            if os.path.isdir(subdir_path):
                for file in os.listdir(subdir_path):
                    shutil.move(os.path.join(subdir_path, file), category_path)
                os.rmdir(subdir_path)
                logger.info(f"Cleaned extension directory: {subdir_path}")


class CategoryFileValidationFilter(Filter):
    """
    Validates that files within categories are correctly placed.
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Validating files within categories.")
        try:
            for category in config.categories:
                category_path = os.path.join(config.dir, category.name)

                if not category.categorize_extensions:
                    # Move files from extension subdirectories to main category dir
                    # and then validate that the main category directory only contains the correct files
                    self._flatten_and_validate_category_dir(
                        category_path, category.extensions)

            return chain.next(config)
        except Exception as e:
            logger.error(f"Error validating files in categories: {str(e)}")
            return FilterResponse("failure", config, str(e))

    def _flatten_and_validate_category_dir(self, category_path, valid_extensions):
        for subdir in os.listdir(category_path):
            subdir_path = os.path.join(category_path, subdir)
            if os.path.isdir(subdir_path):
                for file in os.listdir(subdir_path):
                    shutil.move(os.path.join(subdir_path, file), category_path)
                os.rmdir(subdir_path)

        # After flattening, validate the files in the main category directory
        for file in os.listdir(category_path):
            if os.path.splitext(file)[-1].lower() not in valid_extensions:
                raise Exception(
                    f"File {file} is not supposed to be in {category_path}")


class MoveFilesToCategoryFilter(Filter):
    """
    Moves files to their respective category directories.
    """

    def do_filter(self, config: Config, chain: FilterChain) -> FilterResponse:
        logger.debug("Moving files to their respective category directories.")
        try:
            all_files = [f for f in os.listdir(
                config.dir) if os.path.isfile(os.path.join(config.dir, f))]

            for file in all_files:
                file_moved = False
                file_ext = os.path.splitext(file)[-1].lower()

                for category in config.categories:
                    if file_ext in category.extensions:
                        destination_dir = os.path.join(
                            config.dir, category.name)

                        if category.categorize_extensions:
                            ext_dir = os.path.join(
                                destination_dir, file_ext.lstrip('.'))
                            destination_dir = ext_dir

                        shutil.move(os.path.join(config.dir, file),
                                    os.path.join(destination_dir, file))
                        logger.info(
                            f"Moved {file} to category: {category.name}")
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


def get_organizer_filters() -> List[Filter]:
    return [
        ValidateDirectoryPathFilter(),
        CategoryValidationCreationFilter(),
        CategoryFileValidationFilter(),
        MoveFilesToCategoryFilter()
    ]
