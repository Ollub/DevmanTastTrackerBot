import logging

from requests.exceptions import ReadTimeout, ConnectionError
import telegram
from telegram.ext import Updater, CommandHandler

from settings import CONFIG
from dvmn import poll_dvmn_lesson_info, format_lesson_info
from log import setup_logging


logger = logging.getLogger(__name__)
setup_logging()

updater = Updater(token = CONFIG["BOT_TOKEN"], request_kwargs=CONFIG['PROXY'])
dp = updater.dispatcher


def main():
    logger.info('Bot started')
    while True:
        try:
            dvmn_reply, timestamp = poll_dvmn_lesson_info()
            for lesson_info in dvmn_reply['new_attempts']:
                formated_info = format_lesson_info(lesson_info)
                logger.info(f'Get response from dvmn.org :\n{formated_info}')
                updater.bot.send_message(chat_id=CONFIG['CHAT_ID'], text=formated_info)
        except ReadTimeout:
            logger.error('Timout Error')
        except ConnectionError:
            logger.error('Connection Error')

    dvmn_reply = poll_dvmn_for_status()
    return format_dmvn_reply(dvmn_reply)


if __name__ == '__main__':
    main()