
import logging

from src.logger_config import setup_file_logging
from src.organizer.file_organizer import FileOrganizer



def main():
    setup_file_logging(log_level=logging.DEBUG)

    file_organizer = FileOrganizer()
    file_organizer.run(config_filepath="config.json")


if __name__ == "__main__":
    main()
