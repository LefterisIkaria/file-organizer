"""
Module to process and sort the directories via a json config file.

    Directory Proccess Steps
    --------------------------------------------------------------------
    Step 1. Validate that the directory exists
    Setp 2. Validate that the directory is not a critical directory (like C://Windows, and others for windows, linux, mac)
    Step 3. Validate that have permissions to that directory
    Step 4. Check if any category exists and move all files from the 
            category and subcategories back to the main directory
    Step 5. Create missing categories & one for Uncategorized and one for Hidden files that is a hidden directory
    Step 6. Move files to the appropriate categories/subcategories
    Step 7. Go through all categories/subcategories and delete empty ones
"""

import os
import platform
import shutil

from models import Category, Config

class FileOrganizer:

    CRITICAL_DIRECTORIES = {
        'Windows': ['C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)'],
        'Linux': ['/', '/root', '/etc', '/bin', '/sbin', '/usr/bin', '/usr/sbin'],
        'Darwin': ['/', '/System', '/Library', '/usr', '/bin', '/sbin']
    }

    def __init__(self, directory):
        self.directory = directory

    def validate_directory(self):
        
        if not os.path.exists(self.directory):
            raise ValueError("Directory does not exist")

        os_name = platform.system()  # or another method to get the OS name
        if self.directory in self.CRITICAL_DIRECTORIES.get(os_name, []):
            raise ValueError("Cannot process a critical system directory")

        # Test permissions by trying to list the directory
        try:
            os.listdir(self.directory)
        except PermissionError:
            raise PermissionError("No permissions to access the directory")


    def reset_categories(self, directory: str, categories: list[Category]):
        """
        Move all files from the category directories (and their subdirectories)
        to the main directory and remove the empty subdirectories, but leave
        the main category directory intact.
        
        :param directory: The main directory path.
        :param categories: List of category names.
        """
        for category in categories:
            category_path = os.path.join(directory, category.name)
            
             # Check if the category directory exists
            if os.path.exists(category_path):
                # Recursively walk through the directory
                for root, _, files in os.walk(category_path, topdown=False):  # Using topdown=False to iterate from innermost directory
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Move each file to the main directory
                        shutil.move(file_path, directory)

                    # Check if the directory is empty and it's not the main category directory
                    if not os.listdir(root) and root != category_path:
                        os.rmdir(root)


    def create_categories(self, directory: str, categories: list[Category]):
        """
        Create the main category directories that do not exist. 
        If categorize_extensions is true for a category, create subdirectories for each extension.

        :param directory: The main directory path.
        :param categories: List of category objects.
        """
        for category in categories:
            category_path = os.path.join(directory, category.name)
            
            # Create the main category directory if it doesn't exist
            if not os.path.exists(category_path):
                os.makedirs(category_path)
            
            # If categorize_extensions is true, create subdirectories for each extension
            if category.categorize_extensions:
                for ext in category.extensions:
                    ext_dir = os.path.join(category_path, ext.lstrip('.'))
                    if not os.path.exists(ext_dir):
                        os.makedirs(ext_dir)


    def categorize_files(self, directory: str, categories: list[Category]):
        """
        Categorize files in the main directory based on their extensions.
        
        :param directory: The main directory path.
        :param categories: List of category objects.
        """
        
        # First, let's create a mapping of extensions to their respective categories.
        extension_to_category = {}
        for category in categories:
            for ext in category.extensions:
                extension_to_category[ext] = category
        
        # Now, let's go through each file in the main directory.
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Ensure it's a file and not a directory.
            if not os.path.isfile(file_path):
                continue
            
            # Get the file's extension.
            _, ext = os.path.splitext(filename)
            
            # Determine its category.
            category = extension_to_category.get(ext)
            if not category:
                # If no category exists for the extension, we might want to place it in an 'Uncategorized' folder.
                # This is up to your design.
                continue
            
            # Determine the target directory based on whether we're categorizing by extension.
            if category.categorize_extensions:
                target_directory = os.path.join(directory, category.name, ext.lstrip('.'))
            else:
                target_directory = os.path.join(directory, category.name)
            
            # Move the file to its category directory (or sub-directory).
            shutil.move(file_path, target_directory)


    def cleanup_directory(self, directory: str, categories: list[Category]):
        """
        Delete empty category directories and their empty subdirectories.
        
        :param directory: The main directory path.
        :param categories: List of category objects.
        """
        
        for category in categories:
            category_directory = os.path.join(directory, category.name)
            
            # If we're categorizing by extension, we need to check each subdirectory.
            if category.categorize_extensions:
                for ext in category.extensions:
                    ext_directory = os.path.join(category_directory, ext.lstrip('.'))
                    # If the subdirectory exists and is empty, remove it.
                    if os.path.exists(ext_directory) and not os.listdir(ext_directory):
                        os.rmdir(ext_directory)
            
            # Now, after possibly removing subdirectories, if the category directory is empty, remove it.
            if os.path.exists(category_directory) and not os.listdir(category_directory):
                os.rmdir(category_directory)
    


    def process_config(self, config: Config):
        self.validate_directory(config.directory)
        self.reset_categories(config.directory, config.categories)
        self.create_categories(config.directory, config.categories)
        self.categorize_files(config.directory, config.categories)
        self.cleanup_directory(config.directory, config.categories)