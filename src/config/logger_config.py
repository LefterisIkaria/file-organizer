import os, json
import logging
import logging.config

class ColoredFormatter(logging.Formatter):
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
        log_message = super(ColoredFormatter, self).format(record)
        return (
            f"{self.COLORS['TIMESTAMP']}{self.formatTime(record, self.datefmt)}{self.COLORS['ENDC']} "
            f"{self.COLORS['LEVEL_NAME'].get(record.levelname)}{record.levelname}{self.COLORS['ENDC']} "
            f"{self.COLORS['MESSAGE']}{record.getMessage()}{self.COLORS['ENDC']}"
        )


def setup_logging_from_json(filepath: str):

    log_dir = os.path.join(os.path.expanduser("~"), ".file-organizer", "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    with open(filepath, "r") as f:
        config = json.load(f)

    # Replace {USER_HOME} with the actual path
    for handler in config['handlers'].values():
        if 'filename' in handler:
            handler['filename'] = handler['filename'].format(USER_HOME=log_dir)

    logging.config.dictConfig(config)

     # Create a ColoredFormatter
    colored_formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')

    # Get the root logger
    logger = logging.getLogger()

    # Update the console handler to use the ColoredFormatter
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(colored_formatter)