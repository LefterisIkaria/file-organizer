import os
import json
import logging
import logging.config

from utils import get_resource_path

class ColoredFormatter(logging.Formatter):
    """Class to provide a colored formatter in console logs"""
    COLORS = {
        'TIMESTAMP': '\033[90m',
        'LEVEL_NAME': {
            'WARNING': '\033[93m',
            'INFO': '\033[92m',
            'DEBUG': '\033[94m',
            'CRITICAL': '\033[91m',
            'ERROR': '\033[91m'
        },
        'MESSAGE': '\033[97m',
        'ENDC': '\033[0m'
    }

    def format(self, record):
        return (
            f"{self.COLORS['TIMESTAMP']}{self.formatTime(record, self.datefmt)}{self.COLORS['ENDC']} "
            f"{self.COLORS['LEVEL_NAME'].get(record.levelname)}{record.levelname}{self.COLORS['ENDC']} "
            f"{self.COLORS['MESSAGE']}{record.getMessage()}{self.COLORS['ENDC']}"
        )

def _setup_logging(app_directory: str):
    """Sets up the logging for the app"""

    # Create logs directory
    logs_directory = os.path.join(app_directory, "logs")
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    log_dir = os.path.join(os.path.expanduser("~"), ".file-organizer", "logs")

    with open(get_resource_path("config/logging.json"), "r") as f:
        config = json.load(f)

    for handler in config['handlers'].values():
        if 'filename' in handler:
            handler['filename'] = handler['filename'].format(USER_HOME=log_dir)

    logging.config.dictConfig(config)



def _setup_cofigs_dir(app_directory: str):
    """Sets up the configs directory"""
    configs_directory = os.path.join(app_directory, "configs")
    if not os.path.exists(configs_directory):
        os.makedirs(configs_directory)



def setup_environment():
    """Sets up the application environment in order to run"""
    # User home directory
    home_directory = os.path.expanduser("~")
    # Create .file-organizer directory if it doesn't exist
    app_directory = os.path.join(home_directory, ".file-organizer")
    if not os.path.exists(app_directory):
        os.makedirs(app_directory)

    # Setup configs directory
    _setup_cofigs_dir(app_directory)
    # Setup logging configurations
    _setup_logging(app_directory)


def configs_path():
    """Retrieve the configs path"""
    # User home directory
    home_directory = os.path.expanduser("~")
    # Create .file-organizer directory if it doesn't exist
    return os.path.join(home_directory, ".file-organizer", "configs")