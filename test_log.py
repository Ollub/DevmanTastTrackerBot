import logging
from logging.handlers import RotatingFileHandler

# print(help(RotatingFileHandler))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
fh = 


logger = logging.getLogger("Название логера")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("!!!!!!test!!!!!!.log", maxBytes=200, backupCount=2, encoding='UTF-8')
ch = logging.StreamHandler()
logger.addHandler(handler)

logger.info("Я новый логер!")

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
logging.debug('Сообщение для дебагинга')
logging.info('Произошло какое-то событие. Всё идёт по плану.')
logging.warning('Предупреждение, что-то могло сломаться')
logging.error('Ошибка, что-то сломалось')
logging.critical('МЫ В ОГНЕ ЧТО ДЕЛАТЬ?!?!')
