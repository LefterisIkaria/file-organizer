import os
import shutil
import argparse


def reset_directory(directory: str):
    """
    Resets a directory by moving all files to the main directory
    and deleting all categories and subcategories.
    """
    # List all items in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # If it's a file, continue (because it's already in the main directory)
        if os.path.isfile(item_path):
            continue

        # If it's a directory (category or subcategory)
        if os.path.isdir(item_path):
            # Move all files in this directory to the main directory
            for sub_item in os.listdir(item_path):
                sub_item_path = os.path.join(item_path, sub_item)
                if os.path.isfile(sub_item_path):
                    shutil.move(sub_item_path, directory)
                elif os.path.isdir(sub_item_path):  # It's a subcategory
                    for file in os.listdir(sub_item_path):
                        shutil.move(os.path.join(
                            sub_item_path, file), directory)
                    os.rmdir(sub_item_path)  # Delete the now-empty subcategory
            os.rmdir(item_path)  # Delete the now-empty category


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reset a directory by moving all files to the main directory and deleting all categories and subcategories.")
    parser.add_argument("directory", help="Path to the directory to reset.")
    args = parser.parse_args()

    reset_directory(args.directory)
    print(f"Directory {args.directory} has been reset.")
