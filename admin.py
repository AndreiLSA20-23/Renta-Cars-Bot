from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ParseMode
from config import ADMIN_ID, DB_FILE
from messages import *
import keyboards as kb
from utils import State
from dbWorker import Database
from bot import dp, bot

db = Database(DB_FILE)

# @dp.message_handler(commands=['admin'])
# async def cmd_admin(message: types.Message):
#     await State.adminState.set()
#     await bot.send_message(message.from_user.id, greeting_msg_admin.format(message.from_user), reply_markup=kb.adminMenu)

@dp.message_handler(state=State.adminState)
async def process_admin_menu(message: types.Message, state: FSMContext):
    if message.text == 'Машины в наличии 🎯':
        await state.finish()
        await message.answer('Выберите марку:', reply_markup=kb.modelMenu)
        await State.modelCarAdmin.set()
    if message.text == 'В стартовое меню ⬅️':
        await state.finish()
        await message.answer('Вы переместились в стартовое меню!', reply_markup=kb.startMenu)

@dp.message_handler(state=State.modelCarAdmin)
async def process_model_car_admin(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await state.finish()
        await message.answer('Вы вернулись в админку!', reply_markup=kb.adminMenu)
        await State.adminState.set() 
    elif message.text == 'Range Rover':
        rangeState = State.rangeState
        await carBase(message, state, dp, rangeState, message.text) 
    elif message.text == 'Toyota':
        toyotaState = State.toyotaState
        await carBase(message, state, dp, toyotaState, message.text)
    elif message.text == 'Mitsubishi':
        mitsubishiState = State.mitsubishiState
        await carBase(message, state, dp, mitsubishiState, message.text) 
    elif message.text == 'Mercedes':
        mercedesState = State.mercedesState
        await carBase(message, state, dp, mercedesState, message.text) 
    elif message.text == 'Kia':
        kiaState = State.kiaState
        await carBase(message, state, dp, kiaState, message.text) 
    elif message.text == 'Chevrolet':
        chevroletState = State.chevroletState
        await carBase(message, state, dp, chevroletState, message.text) 
    elif message.text == 'Lexus':
        lexusState = State.lexusState
        await carBase(message, state, dp, lexusState, message.text) 
    elif message.text == 'Hyundai':
        hyundaiState = State.hyundaiState
        await carBase(message, state, dp, hyundaiState, message.text) 

CarID = 0
async def carBase(message: types.Message, state: FSMContext, dp, car, msg):
    result = db.count_car_model(msg)
    await state.finish()
    await message.answer(f'Вы выбрали машины маркой {msg}', reply_markup=kb.cancelMenu) 
    await car.set()
    @dp.message_handler(state=car)
    async def process_car(message: types.Message, state: FSMContext):
        if message.text == 'Назад ⬅️':
            global CarID
            CarID = 0
            await state.finish()
            await message.answer('Вы вернулись в меню марок!', reply_markup=kb.modelMenu)
            await State.modelCarAdmin.set()
        else:
            await message.answer('Вы хотите вернуться назад? Нажмите на кнопку ниже!')

    await message.answer(f'*{result[CarID][0]}*\nВ наличии данная машина?', reply_markup=kb.stockMenu, parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query_handler(state=car)   
    async def process_callback_car(call: types.CallbackQuery): 
        global CarID
        if call.data == 'NextCar':
            if CarID == len(result)-1:
                CarID = 0
                await message.answer(f'*{result[CarID][0]}*\nВ наличии данная машина?', reply_markup=kb.stockMenu, parse_mode=ParseMode.MARKDOWN)
                await call.message.delete()
            else:
                CarID += 1
                await message.answer(f'*{result[CarID][0]}*\nВ наличии данная машина?', reply_markup=kb.stockMenu, parse_mode=ParseMode.MARKDOWN)
                await call.message.delete()
        elif call.data == 'stockCar':
            db.set_in_stock(result[CarID][0])
            await message.answer(f'*{result[CarID][0]}* теперь в наличии!', parse_mode=ParseMode.MARKDOWN)
            CarID = 0
        elif call.data == 'outOfStockCar':
            db.set_out_of_stock(result[CarID][0])
            await message.answer(f'*{result[CarID][0]}* теперь не в наличии!', parse_mode=ParseMode.MARKDOWN)
            CarID = 0