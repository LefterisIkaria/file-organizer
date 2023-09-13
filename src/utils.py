import json
import os
import platform
import logging
import sys

from models import Config

LOG = logging.getLogger(__name__)


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


def get_resource_path(relative_path: str) -> str:
    # Determine if the application is bundled
    bundled = getattr(sys, 'frozen', False)
    
    if bundled:
        # If bundled, adjust the path to the location of the bundled data
        base_path = sys._MEIPASS
        return os.path.join(base_path, relative_path)
    else:
        # Otherwise, use the current directory (typical during development)
        # base_path = os.path.dirname(os.path.abspath(__file__))
        return relative_path
    


def get_template_config() -> Config | None:
    with open(get_resource_path("config/template.json"), "r") as f:
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