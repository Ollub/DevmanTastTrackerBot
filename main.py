import logging

from requests.exceptions import ReadTimeout, ConnectionError
import telegram
from telegram.ext import Updater, CommandHandler
from requests.exceptions import HTTPError

from settings import CONFIG
from dvmn import poll_dvmn_lesson_info, format_lesson_info

from log import setup_logging, get_logger


logger = logging.getLogger(__name__)

updater = Updater(token = CONFIG["BOT_TOKEN"], request_kwargs=CONFIG['PROXY'])
dp = updater.dispatcher

#logging bot initialization
log_bot_updater = Updater(token = CONFIG["LOG_BOT_TOKEN"], request_kwargs=CONFIG['PROXY'])

def main():
    setup_logging()
    logger = get_logger(log_bot_updater, CONFIG['CHAT_ID'], 'my_logger')
    logger.info('Bot started')

    # start polling dvmn API
    timestamp = None
    while True:
        try:
            lessons_info, timestamp = poll_dvmn_lesson_info(timestamp=timestamp)
        except ReadTimeout:
            continue
        except ConnectionError:
            logger.error('Connection Error')
        except HTTPError:
            logger.error('HTTPError')
        except Exception:
            logger.error('Unexpected exception!', exc_info=True)
        else:
            for lesson_info in lessons_info or []:
                logger.info(f'Get lesson info from dvmn.org :\n{lesson_info}')
                formated_info = format_lesson_info(lesson_info)
                updater.bot.send_message(chat_id=CONFIG['CHAT_ID'], text=formated_info)


if __name__ == '__main__':
    main()
