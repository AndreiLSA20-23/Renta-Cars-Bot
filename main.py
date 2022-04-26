import asyncio
import logging
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import *

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, loop=loop, storage=storage)  
from bot import RentaBot

RentaBot(dp, bot).start_btn()

if __name__ == '__main__':
    executor.start_polling(dp)