import logging

from requests.exceptions import ReadTimeout, ConnectionError
import telegram
from telegram.ext import Updater, CommandHandler
from requests.exceptions import HTTPError

from settings import CONFIG
from dvmn import poll_dvmn_lesson_info, format_lesson_info
from log import setup_logging


logger = logging.getLogger(__name__)

updater = Updater(token = CONFIG["BOT_TOKEN"], request_kwargs=CONFIG['PROXY'])
dp = updater.dispatcher


def main():
    setup_logging()
    logger.info('Bot started')
    timestamp = None
    #start polling dvmn API
    while True:
        try:
            lessons_info, timestamp = poll_dvmn_lesson_info(timestamp=timestamp)
            if not lessons_info:
                continue
            for lesson_info in lessons_info:
                logger.info(f'Get lesson info from dvmn.org :\n{lesson_info}')
                formated_info = format_lesson_info(lesson_info)
                updater.bot.send_message(chat_id=CONFIG['CHAT_ID'], text=formated_info)
        except ReadTimeout:
            continue
        except ConnectionError:
            logger.error('Connection Error')
        except HTTPError:
            logger.error('HTTPError')


if __name__ == '__main__':
    main()
