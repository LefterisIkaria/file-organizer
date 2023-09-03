import argparse
import logging
import os
import shutil
from src.gui.app import App
from src.config.logger_config import setup_logging_from_json
from src.organizer.file_organizer import FileOrganizer
from src.utils.reset_directory import reset_directory

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="File Organizer Application")
    parser.add_argument("--gui", action="store_true", help="Start the GUI")
    parser.add_argument("--organize", action="store_true", help="Run the file organizer")
    parser.add_argument("--reset", action="store_true", help="Reset a directory")
    parser.add_argument("--directory", type=str, help="Directory to reset")
    return parser.parse_args()

# def setup():
#     user_home = os.path.expanduser("~")
#     app_dir = os.path.join(user_home, ".file-organizer")
#     config_path = os.path.join(app_dir, "app.json")
#     template_path = "config/app.template.json"

#     # Create the directory if it doesn't exist
#     if not os.path.exists(app_dir):
#         os.makedirs(app_dir)

#     # Check if app.json exists
#     if not os.path.exists(config_path):
#         # Copy app.template.json to app.json
#         shutil.copy(template_path, config_path)

def get_config_path():
    home_path = os.path.expanduser("~")
    return os.path.join(home_path, ".file-organizer", "app.json")

def main():
    setup_logging_from_json("config/logging.json")
    args = parse_args()

    if args.gui:
        logger.info("Starting GUI...")
        app = App()
        app.mainloop()
    elif args.organize:
        logger.info("Running the file organizer script...")
        app_config_path = get_config_path()
        organizer = FileOrganizer()
        organizer.run(app_config_path)
    elif args.reset:
        if args.directory:
            logger.info(f"Running the reset directory script on {args.directory}...")
            reset_directory(args.directory)
        else:
            logger.warning("Directory not specified for reset. Use --directory to specify the directory.")
    else:
        logger.warning("No action specified. Use --gui to start the GUI or --organize to run the file organizer.")

if __name__ == "__main__":
   
    main()
