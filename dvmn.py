import requests
import logging
import time
import os

from settings import CONFIG


logger = logging.getLogger(__name__)


def poll_dvmn_lesson_info(timestamp=None, timeout=120):
    '''
    Function polls DVMN API till get lesson info
    '''
    url = 'https://dvmn.org/api/long_polling/'
    headers = {"Authorization": f"Token {CONFIG['DVMN_TOKEN']}"}
    params = {'timestamp': timestamp}

    logger.debug(f'Start polling with timestamp {timestamp}')
    start_time = time.time()
    response = requests.get(url, headers=headers, params=params, timeout=timeout)
    logger.debug("Polling time = {}".format(start_time - time.time()))

    if response.json()['status'] == 'timeout':  #no updates ==> continue polling from stop point
        timestamp = response.json()['timestamp_to_request']
        poll_dvmn_lesson_info(timestamp)
    
    timestamp = response.json()['last_attempt_timestamp']
    return response.json(), timestamp


def format_lesson_info(lesson_info):
    lesson_title = lesson_info['lesson_title']
    if lesson_info['is_negative']:
        lesson_status = 'К сожалению в работе нашлись ошибки'
    else:
        lesson_status = 'Работа принята'
    return f'У вас проверили работу "{lesson_title}". \n\n{lesson_status}'