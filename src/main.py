import argparse
import logging
import os
import shutil
from src.models.config_manager import ConfigManager
from src.organizer.scheduler import Scheduler
from src.gui.app import App
from src.config.logger_config import setup_logging_from_json
from src.organizer.file_organizer import FileOrganizer
from src.utils.reset_directory import reset_directory

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="File Organizer Application")
    parser.add_argument("--gui", action="store_true", help="Start the GUI")
    parser.add_argument("--organizer", action="store_true", help="Run the file organizer")
    parser.add_argument("--scheduler", action="store_true", help="Run scheduler")
    parser.add_argument("--reset", action="store_true", help="Reset a directory")
    parser.add_argument("--directory", type=str, help="Directory to reset")
    return parser.parse_args()

def setup():
    user_home = os.path.expanduser("~")
    app_dir = os.path.join(user_home, ".file-organizer")
    config_path = os.path.join(app_dir, "app.json")
    template_path = "config/app.template.json"

    # Create the directory if it doesn't exist
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)

    # Check if app.json exists
    if not os.path.exists(config_path):
        # Copy app.template.json to app.json
        shutil.copy(template_path, config_path)

def get_config_path():
    home_path = os.path.expanduser("~")
    return os.path.join(home_path, ".file-organizer", "app.json")

def run_gui(config_manager: ConfigManager):
    logger.info("Starting GUI...")
    app = App(config_manager, themename="darkly", )
    app.mainloop()


def run_organizer(config_manager: ConfigManager):
    logger.info("Running the file organizer script...")
    organizer = FileOrganizer(config_manager)
    organizer.process_all()


def run_reset_directory(dir: str):
    logger.info(f"Running the reset directory script on {dir}...")
    reset_directory(dir)


def run_scheduler(config_manager: ConfigManager):
    configs = config_manager.get_configs()
    for config in configs:
        schedule = config.schedule
        
        organizer = FileOrganizer(config_manager)
        scheduler = Scheduler(schedule)
        scheduler.run_task(organizer.process_all)
        scheduler.start()
        logger.info(f"Scheduling the file organizer to run every {schedule.interval} {schedule.type.name.lower()}(s)...")


def main():
    setup()
    setup_logging_from_json("config/logging.json")
    
    config_manager = ConfigManager(get_config_path())
    args = parse_args()

    if args.gui:
       run_gui(config_manager)
    elif args.organizer:
       run_organizer(config_manager)
    elif args.reset:
        if args.directory:
            run_reset_directory(args.directory)
        else:
            logger.warning("Directory not specified for reset. Use --directory to specify the directory.")
    elif args.scheduler:
        run_scheduler(config_manager)
    else:
        logger.warning("No action specified. Use --gui to start the GUI or --organize to run the file organizer.")

if __name__ == "__main__":
   
    main()
