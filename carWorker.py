import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from config import *
from messages import *
import keyboards as kb
from utils import State
from dbWorker import Database
from order import BuyCar

db = Database(DB_FILE)
CarID = 0

class CarRecognizer:
    def __init__(self, dp, bot, modelState, model, result):
        self.dp = dp
        self.bot = bot
        self.modelState = modelState
        self.model = model
        self.result = result
    
    async def getPrices(self):
        firstPrice = re.split('в|/',self.result[CarID][4])[0] + firstTerm
        secondPrice = re.split('в|/',self.result[CarID][4])[1].replace(' сутки25 суток-месяц ', '') + secondTerm
        thirdPrice = re.split('в|/',self.result[CarID][4])[2].replace(' сутки15-24 суток ', '') + thirdTerm
        fourthPrice = re.split('в|/',self.result[CarID][4])[3].replace(' сутки7-14 суток ', '') + fourtTerm
        fifthPrice = re.split('в|/',self.result[CarID][4])[4].replace(' сутки3-6 суток ', '') + fifthTerm
        pricesAll = firstPrice+'\n'+secondPrice+'\n'+thirdPrice+'\n'+fourthPrice+'\n'+fifthPrice
        return pricesAll

    async def sendCar(self, CarID, message: types.Message):
        prices = await self.getPrices()
        await message.answer_photo(self.result[CarID][8], 
        caption=CarCaption.format(name=self.result[CarID][0], amount=self.result[CarID][1], fuel=self.result[CarID][2], trans=self.result[CarID][3], prices=prices, deposit=self.result[CarID][5], charblock=self.result[CarID][6]),
        reply_markup=kb.carMenu)

    async def getCar(self, message: types.Message, state: FSMContext):
        await state.finish()
        await message.answer(f'Вы выбрали машины маркой {self.model}', reply_markup=kb.cancelMenu) 
        await self.modelState.set()
        @self.dp.message_handler(state=self.modelState)
        async def process_car_navigation(message: types.Message):
            if message.text == 'Назад ⬅️':
                global CarID
                CarID = 0
                await state.finish()
                await message.answer('Вы вернулись в меню марок!', reply_markup=kb.modelMenu)
                await State.modelCar.set()
            else:
                await message.answer('Вы хотите вернуться назад? Нажмите на кнопку ниже!')

        await self.sendCar(CarID, message)

        @self.dp.callback_query_handler(state=self.modelState)   
        async def process_callback_car_nav(call: types.CallbackQuery):
            global CarID
            if call.data == 'OrderCar':
                await state.finish()
                await call.message.answer('Чтобы заказать машину, надо выбрать срок использование!', reply_markup=kb.dateMenu)
                await State.buyState.set()
            
                order = BuyCar(self.dp, self.bot, self.result, CarID)
                await order.getDate()
                
                CarID = 0
            elif call.data == 'NextCar':
                if CarID == len(self.result)-1:
                    CarID = 0
                    await self.sendCar(CarID, message)
                    await call.message.delete()  
                else:
                    CarID += 1
                    await self.sendCar(CarID, message)
                    await call.message.delete()