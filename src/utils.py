import json
import os
import platform
import logging
import sys

from models import Config

LOG = logging.getLogger(__name__)


def clear_console():
    """
    Clear the terminal/console screen based on the operating system.
    """
    system_name = platform.system()

    if system_name == "Windows":
        # Windows
        os.system('cls')
    elif system_name in ["Linux", "Darwin"]:
        # Linux and MacOs
        os.system('clear')
    else:
        print(f"Doesn't support this operating system: {system_name}")


def get_resource_path(relative_path: str) -> str:
    """
    Get the resource path for a given relative path. 
    Adjusts the path based on whether the app is bundled or running in development mode.
    
    Args:
        relative_path (str): The relative path of the resource.
        
    Returns:
        str: The adjusted path to the resource.
    """

    # Determine if the application is bundled
    bundled = getattr(sys, 'frozen', False)
    
    if bundled:
        # If bundled, adjust the path to the location of the bundled data
        base_path = sys._MEIPASS
        return os.path.join(base_path, relative_path)
    else:
        # Otherwise, use the current directory (typical during development)
        return relative_path
    


def get_template_config() -> Config | None:
    """
    Load and return the template configuration from a JSON file.
    
    Returns:
        Config: The loaded configuration object.
        None: If there's any error during the loading process.
    """
    with open(get_resource_path("config/template.json"), "r") as f:
        try:
            data = json.load(f)
            return Config.from_dict(data)
        except Exception as e:
            LOG.error(e)
            return None


class Table:
    """
    Represents a table for displaying data in the terminal.
    
    Attributes:
        headers (list[str] | tuple[str]): The headers for the table columns.
        data (list[tuple[str]]): The data rows of the table.
    """

    def __init__(self, headers: list[str] | tuple[str], data: list[tuple[str]]) -> None:
        self.headers = ["#"] + headers
        self.set_data(data)
        
        self.column_widths = self._compute_column_widths()
    

    def set_data(self, data: list[tuple[str]]):
        """
        Set the data for the table, adding an index to each row.
        
        Args:
            data (list[tuple[str]]): The data rows to set.
        """
        self.data = [(str(i+1),) + row for i, row in enumerate(data)]
    

    def _compute_column_widths(self):
       """
        Compute the widths for each column based on the maximum content length in each column.
        
        Returns:
            list[int]: The computed widths for each column.
        """
       return [max(len(str(item[col_idx])) for item in [self.headers] + self.data) for col_idx in range(len(self.headers))]
    

    def draw_table(self):
        """
        Display the table in the terminal.
        """

        header_row = " | ".join([self.headers[col_idx].ljust(self.column_widths[col_idx]) for col_idx in range(len(self.headers))])
        divider = "-+-".join(["-" * self.column_widths[col_idx] for col_idx in range(len(self.headers))])

        print(divider)
        print(header_row)
        print(divider)
        for row in self.data:
            print(" | ".join([str(row[col_idx]).ljust(self.column_widths[col_idx]) for col_idx in range(len(self.headers))]))
            print(divider)
    

    def get_row(self, idx: int):
        """
        Retrieve a specific row from the table data by index.
        
        Args:
            idx (int): The index of the row to retrieve.
            
        Returns:
            tuple[str]: The retrieved row.
            None: If the index is out of bounds.
        """
        return self.data[idx] if idx < len(self.data) else None
    
    def empty(self):
        """
        Determine if the table has no data.
        
        Returns:
            bool: True if the table has no data, False otherwise.
        """
        return len(self.data) == 0