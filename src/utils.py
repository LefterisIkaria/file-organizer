import json
import os
import platform
import shutil
import logging

from src.models import Config

LOG = logging.getLogger(__name__)

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


def clear_console():
    system_name = platform.system()

    if system_name == "Windows":
        # Windows
        os.system('cls')
    elif system_name in ["Linux", "Darwin"]:
        # Linux and MacOs
        os.system('clear')
    else:
        print(f"Doesn't support this operating system: {system_name}")


def get_template_config() -> Config | None:
    with open("config/template.json", "r") as f:
        try:
            data = json.load(f)
            return Config.from_dict(data)
        except Exception as e:
            LOG.error(e)
            return None



class Table:

    def __init__(self, headers: list[str] | tuple[str], data: list[tuple[str]]) -> None:
        self.headers = ["#"] + headers
        self.set_data(data)
        
        self.column_widths = self._compute_column_widths()
    

    def set_data(self, data: list[tuple[str]]):
        self.data = [(str(i+1),) + row for i, row in enumerate(data)]
    

    def _compute_column_widths(self):
       # Determine column widths
       column_widths = [max(len(str(item[col_idx])) for item in [self.headers] + self.data) for col_idx in range(len(self.headers))]
       return column_widths
    

    def draw_table(self):
        # Draw the table
        header_row = " | ".join([self.headers[col_idx].ljust(self.column_widths[col_idx]) for col_idx in range(len(self.headers))])
        divider = "-+-".join(["-" * self.column_widths[col_idx] for col_idx in range(len(self.headers))])

        print(divider)
        print(header_row)
        print(divider)
        for row in self.data:
            print(" | ".join([str(row[col_idx]).ljust(self.column_widths[col_idx]) for col_idx in range(len(self.headers))]))
            print(divider)
    

    def get_row(self, idx: int):
        return self.data[idx] if idx < len(self.data) else None
    
    def empty(self):
        return len(self.data) == 0