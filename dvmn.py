import requests
import logging
import time
import os

from settings import CONFIG


logger = logging.getLogger(__name__)


def poll_dvmn_lesson_info(timestamp=None, timeout=100):
    """Function polls DVMN API for getting lesson info

    Keyword arguments:
    timestamp - timestamp of last response from server
    timeout - typical timout for dvmn server 90sec, but it can change
    """
    url = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": f"Token {CONFIG['DVMN_TOKEN']}"}
    params = {'timestamp': timestamp}

    logger.debug(f'Start polling with timestamp {timestamp}')
    start_time = time.time()
    response = requests.get(url, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    logger.debug("Polling time = {}".format(start_time - time.time()))

    timestamp = response.json().get('last_attempt_timestamp') or\
                response.json().get('timestamp_to_request')
    lessons_info = response.json().get('new_attempts')
    return lessons_info, timestamp


def format_lesson_info(lesson_info):
    lesson_title = lesson_info['lesson_title']
    if lesson_info['is_negative']:
        lesson_status = 'К сожалению в работе нашлись ошибки'
    else:
        lesson_status = 'Работа принята'
    return f'У вас проверили работу "{lesson_title}". \n\n{lesson_status}'
