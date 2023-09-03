import logging

from logging.handlers import RotatingFileHandler


def setup_file_logging(filename='app.log', log_level=logging.INFO, max_log_size=5*1024*1024, backup_count=3):
    logger = logging.getLogger()

    if not logger.handlers:
        logger.setLevel(log_level)

        file_handler = RotatingFileHandler('logs/' + filename, maxBytes=max_log_size, backupCount=backup_count)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(file_formatter)
        # logger.addHandler(stream_handler)

    return logger
