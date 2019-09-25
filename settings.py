import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'DVMN_TOKEN': os.getenv('DVMN_TOKEN'),
    'LOG_BOT_TOKEN': os.getenv('LOG_BOT_TOKEN'),
    'BOT_TOKEN': os.getenv('BOT_TOKEN'),
    'CHAT_ID': os.getenv('CHAT_ID'),
    'PROXY': {
        'proxy_url': os.getenv('PROXY_URL'),
        'urllib3_proxy_kwargs': {'username': os.getenv('PROXY_USERNAME'), 'password': os.getenv('PROXY_PASSWORD')},
        } or None,
    }
