import logging


class LoggerConfig:

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def setup_file_logging(self, filename='app.log'):
        file_handler = logging.FileHandler(filename, mode='a')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def setup_terminal_logging(self):
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
