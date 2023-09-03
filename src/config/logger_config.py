import os, json, sys
import logging
import logging.config

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
