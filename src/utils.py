import os
import platform
import shutil


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


def draw_table(headers: list[str], data: list[list[str]]):

     # Determine column widths
    column_widths = [max(len(item[col_idx]) for item in [headers] + data) for col_idx in range(len(headers))]
    
    # Draw the table
    header_row = " | ".join([headers[col_idx].ljust(column_widths[col_idx]) for col_idx in range(len(headers))])
    divider = "-+-".join(["-" * column_widths[col_idx] for col_idx in range(len(headers))])
    
    print(divider)
    print(header_row)
    print(divider)
    for row in data:
        print(" | ".join([row[col_idx].ljust(column_widths[col_idx]) for col_idx in range(len(headers))]))
        print(divider)