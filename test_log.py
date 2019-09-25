import logging
from logging.handlers import RotatingFileHandler


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

    def get_logger(self):
        print(self.updater, self.chat_id)


def setup_logging(updater, chat_id, logger_name=__name__):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    bh = BotHandler(updater, chat_id)
    bh.setLevel(logging.INFO)
    bh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(bh)
