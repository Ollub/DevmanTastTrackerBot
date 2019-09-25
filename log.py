import os
import logging
import logging.config

import yaml

class BotHandler(logging.Handler):
    """
    Telegram bot handler.
    Takes instance of telegram.ext.Updater and chat_id as attribute
    and sends logs as text messages to the chat using updater.
    """
    def __init__(self, updater, chat_id, *args, **kwargs):
        self.updater = updater
        self.chat_id = chat_id
        super().__init__(*args, **kwargs)

    def emit(self, record):
        log_entry = self.format(record)
        self.updater.bot.send_message(chat_id=self.chat_id, text=log_entry)


def setup_logging(
    default_path='logging.yaml',
    defualt_level=logging.INFO,
    env_key='LOG_CFG'
    ):
    """Setup logging configuration from logging.yaml config file.

    Keyword arguments:
    defaulth_path -- config .yaml file path (default logging.yaml)
    default_level -- default logging level (default logging.INFO)
    env_key -- environment variable name for logging config file path
    """
    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=defualt_level)


def get_logger(updater, chat_id, logger_name, defualt_level=logging.INFO):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    bh = BotHandler(updater, chat_id)
    bh.setLevel(defualt_level)
    bh.setFormatter(formatter)

    logger.addHandler(bh)

    return logger
