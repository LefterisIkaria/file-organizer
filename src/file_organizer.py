"""
Module to process and sort the directories via a json config file.

    Directory Proccess Steps
    --------------------------------------------------------------------
    Step 1. Validations:
        - Validates that the directory exists
        - Validates that the directory is not a critical directory (like C://Windows, and others for windows, linux, mac)
        - Validates that have permissions to sort that directory
    
    Step 2. Check if any category exists and move all files from the category and subcategories back to the main directory
    
    Step 3. Create missing categories plus `Uncategorized` and `.hidden`, one for files that have no category 
            and one for files that are hidden.

    Step 6. Move files to the appropriate categories/subcategories

    Step 7. Check any categories/subcategories and remove empty ones.
"""

import os
import platform
import shutil
import logging

from models import Category, Config


LOG = logging.getLogger(__name__)


class FileOrganizer:

    CRITICAL_DIRECTORIES = {
        'Windows': ['C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)'],
        'Linux': ['/', '/root', '/etc', '/bin', '/sbin', '/usr/bin', '/usr/sbin'],
        'Darwin': ['/', '/System', '/Library', '/usr', '/bin', '/sbin']
    }

    SPECIAL_CATEGORIES = [
        Category(name="Uncategorized", extensions=[], categorize_extensions=False),
        Category(name=".hidden", extensions=[], categorize_extensions=False)
    ]


    def validate_directory(self, directory: str):
        """
        Validates the directory existance, permissions and if it is
        a critical directory that shouldn't change it's structure
        """
        if not os.path.exists(directory):
            LOG.error(f"Directory {directory} does not exist!")
            raise ValueError("Directory does not exist")

        os_name = platform.system()  # method to get the OS name
        if directory in self.CRITICAL_DIRECTORIES.get(os_name, []):
            LOG.error(f"Attempted to process critical system directory: {directory}")
            raise ValueError("Cannot process a critical system directory")

        # Test permissions by trying to list the directory
        if not os.access(directory, os.R_OK | os.W_OK):
            LOG.error(f"No permission to access the directory: {directory}")
            raise PermissionError("No permission to access the directory")


    def reset_directory(self, directory: str, categories: list[Category]):
        """
        Move all files from the category directories (and their subdirectories)
        to the main directory and remove the empty subdirectories, but leave
        the main category directory intact.
        
        :param directory: The main directory path.
        :param categories: List of category names.
        """

        for category in categories + self.SPECIAL_CATEGORIES:

            # Create the path to the category
            category_path = os.path.join(directory, category.name)
            
             # Check if the category directory exists
            if os.path.exists(category_path):
                # Recursively walk through the directory
                for root, _, files in os.walk(category_path, topdown=False):  # Using topdown=False to iterate from innermost directory
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            # Move each file to the main directory
                            shutil.move(file_path, directory)
                            LOG.info(f"Moved {file} from {root} to {directory}")
                        except Exception as e:
                            LOG.error(f"Error moving {file} to main directory: {e}")

                    # Check if the directory is empty and it's not the main category directory
                    if not os.listdir(root) and root != category_path:
                        try:
                            os.rmdir(root)
                        except Exception as e:
                            LOG.error(f"Error removing directory {root}: {e}")


    def create_categories(self, directory: str, categories: list[Category]):
        """
        Create the main category directories that do not exist. 
        If categorize_extensions is true for a category, create subdirectories for each extension.

        :param directory: The main directory path.
        :param categories: List of category objects.
        """
        for category in categories + self.SPECIAL_CATEGORIES:

            # Get category path
            category_path = os.path.join(directory, category.name)
            
            # Create the main category directory if it doesn't exist
            if not os.path.exists(category_path):
                try:
                    os.makedirs(category_path)
                    LOG.info(f"Created category directory {category_path}")
                except Exception as e:
                    LOG.error(f"Error creating directory {category_path}: {e}")
            
            # If categorize_extensions is true, create subdirectories for each extension
            if category.categorize_extensions:
                for ext in category.extensions:
                    ext_dir = os.path.join(category_path, ext.lstrip('.'))
                    if not os.path.exists(ext_dir):
                        try:
                            os.makedirs(ext_dir)
                            LOG.info(f"Created extension subdirectory {ext_dir}")
                        except Exception as e:
                            LOG.error(f"Error creating extension subdirectory {ext_dir}: {e}")


    def categorize_files(self, directory: str, categories: list[Category]):
        """
        Categorize files in the main directory based on their extensions.
        
        :param directory: The main directory path.
        :param categories: List of category objects.
        """
        
       # Create a mapping of extensions to their respective categories.
        extension_to_category = {}
        for category in categories + self.SPECIAL_CATEGORIES:
            for ext in category.extensions:
                extension_to_category[ext] = category
        
        # Go through each file in the main directory.
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Ensure it's a file and not a directory.
            if not os.path.isfile(file_path):
                LOG.debug(f"Skipping {file_path} directory")
                continue
            
            # If the file starts with a dot (i.e., it's hidden), move to ".hidden" directory.
            if filename.startswith('.'):
                LOG.warning(f"File {filename} is a hidden file")
                target_directory = os.path.join(directory, ".hidden")
                try:
                    shutil.move(file_path, target_directory)
                    LOG.info(f"Moved {filename} to {target_directory}")
                    continue
                except Exception as e:
                    LOG.error(f"Error moving {filename} to {target_directory}: {e}")
            
            # Get the file's extension.
            _, ext = os.path.splitext(filename)
            
            # Determine its category.
            category = extension_to_category.get(ext)
            if not category:
                # If the extension doesn't match any category, move to "Uncategorized" directory.
                LOG.warning(f"File {filename} has no category")
                target_directory = os.path.join(directory, "Uncategorized")
            else:
                # Determine the target directory based on whether we're categorizing by extension.
                if category.categorize_extensions:
                    LOG.info(f"Category {category.name} will categorize extensions")
                    target_directory = os.path.join(directory, category.name, ext.lstrip('.'))
                else:
                    target_directory = os.path.join(directory, category.name)
            
            # Move the file to its category directory (or sub-directory).
            try:
                shutil.move(file_path, target_directory)
                LOG.info(f"Moved {filename} to {target_directory}")
            except Exception as e:
                LOG.error(f"Error moving {filename} to {target_directory}: {e}")


    def cleanup_directory(self, directory: str, categories: list[Category]):
        """
        Delete empty category directories and their empty subdirectories.
        
        :param directory: The main directory path.
        :param categories: List of category objects.
        """
        
        for category in categories + self.SPECIAL_CATEGORIES:

            # Get category path
            category_directory = os.path.join(directory, category.name)
            
            # If we're categorizing by extension, we need to check each subdirectory.
            if category.categorize_extensions:
                for ext in category.extensions:
                    ext_directory = os.path.join(category_directory, ext.lstrip('.'))
                    # If the subdirectory exists and is empty, remove it.
                    if os.path.exists(ext_directory) and not os.listdir(ext_directory):
                        try:
                            os.rmdir(ext_directory)
                            LOG.info(f"Removed empty directory {ext_directory}")
                        except Exception as e:
                            LOG.error(f"Error removing directory {ext_directory}: {e}")

            # Now, after possibly removing subdirectories, if the category directory is empty, remove it.
            if os.path.exists(category_directory) and not os.listdir(category_directory):
                try:
                    os.rmdir(category_directory)
                    LOG.info(f"Removed empty category directory {category_directory}")
                except Exception as e:
                    LOG.error(f"Error removing directory {category_directory}: {e}")


    def process_config(self, config: Config):
        
        if not config.active:
            LOG.info(f"Config for directory {config.directory} is inactive, skipping...")
            return
        try:
            self.validate_directory(config.directory)
        except Exception as e:
            LOG.warning(f"Skipping this directory {config.directory}")
            return
        
        self.reset_directory(config.directory, config.categories)
        self.create_categories(config.directory, config.categories)
        self.categorize_files(config.directory, config.categories)
        self.cleanup_directory(config.directory, config.categories)

    
    def process_configs(self, configs: list[Config]):
        for config in configs:
            self.process_config(config)