import argparse
from gui.app import App
from src.config.logger_config import setup_file_logging
from src.organizer.file_organizer import FileOrganizer
from src.utils.reset_directory import reset_directory

def parse_args():
    parser = argparse.ArgumentParser(description="File Organizer Application")
    parser.add_argument("--gui", action="store_true", help="Start the GUI")
    parser.add_argument("--organize", action="store_true", help="Run the file organizer")
    parser.add_argument("--reset", action="store_true", help="Reset a directory")
    parser.add_argument("--directory", type=str, help="Directory to reset")
    return parser.parse_args()

def main():
    logger = setup_file_logging()

    args = parse_args()

    if args.gui:
        logger.info("Starting GUI...")
        app = App()
        app.mainloop()
    elif args.organize:
        logger.info("Running the file organizer script...")
        organizer = FileOrganizer()
        organizer.run("config/config.json")
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
