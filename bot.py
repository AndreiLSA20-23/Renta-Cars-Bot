import asyncio
import logging
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import *
from messages import *
import keyboards as kb
from utils import State
from dbWorker import Database
from carWorker import CarRecognizer

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)  
db = Database(DB_FILE)

#start bot
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await State.adminState.set()
        await bot.send_message(message.from_user.id, greeting_msg_admin.format(message.from_user), reply_markup=kb.adminMenu)
    else:
        await bot.send_message(message.from_user.id, greeting_msg.format(message.from_user), reply_markup=kb.startMenu)

@dp.message_handler(commands=['cancel'])
async def cmd_cancel(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы отменили заказ!', reply_markup=kb.startMenu)

@dp.message_handler()
async def process_startMenu(message: types.Message):
    if message.text == 'Меню 🚘':
        await State.menuState.set()
        await message.answer(menu_msg, reply_markup=kb.mainMenu)   
    elif message.text == 'О нас 💬':
        await message.answer('Тут будет текст про нас.')
    elif message.text == 'Контакты 📞':
        await message.answer('Наши контакты:')
        await message.answer_contact(phone_number='+71737185717851', first_name='RENTACAR’S', reply_markup=kb.contactMenu)
    elif message.text == 'Связь с менеджером 📲':
        await State.communicationState.set()
        await message.answer('Оставьте свои контакты и наш менеджер свяжется с вами в ближайшее время 🤗', reply_markup=kb.communicationMenu)

@dp.message_handler(state=State.menuState)
async def process_menu_btn(message: types.Message, state: FSMContext):
    if message.text == 'Каталог машин 🚛':
        await state.finish()
        await State.modelCar.set()
        await message.answer('Выберите марку:', reply_markup=kb.modelMenu)
    elif message.text == 'Заказать машину прямо сейчас 🚀':
        await state.finish()
        await State.rightNow.set()
        await message.answer('Выберите марку:', reply_markup=kb.modelMenu)
    elif message.text == 'Машины в наличии 🚨':
        await state.finish()
        await State.carStock.set()
        await message.answer('Выберите марку:', reply_markup=kb.modelMenu)
    elif message.text == 'Связь с менеджером 📲':
        await message.answer('Оставьте свои контакты и наш менеджер свяжется с вами в ближайшее время 🤗', reply_markup=kb.communicationMenu)
        await state.finish()
        await State.communicationState.set()
    elif message.text == 'Назад ⬅️':
        await message.answer('Вы вернулись в стартовое меню!', reply_markup=kb.startMenu)
        await state.finish()
    else: 
        await message.answer('Нету такой кнопки!')

#catalog
@dp.message_handler(state=State.modelCar)
async def process_model_car(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await state.finish()
        await message.answer('Вы вернулись в меню!', reply_markup=kb.mainMenu)
        await State.menuState.set() 
    elif message.text == 'Range Rover':
        rangeState = State.rangeState
        result = db.count_car_model(message.text)
        recognizer = CarRecognizer(dp, bot, rangeState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Toyota':
        toyotaState = State.toyotaState
        result = db.count_car_model(message.text)
        recognizer = CarRecognizer(dp, bot, toyotaState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Mitsubishi':
        mitsubishiState = State.mitsubishiState
        result = db.count_car_model(message.text)
        recognizer = CarRecognizer(dp, bot, mitsubishiState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Mercedes':
        mercedesState = State.mercedesState
        result = db.count_car_model(message.text)
        recognizer = CarRecognizer(dp, bot, mercedesState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Kia':
        kiaState = State.kiaState
        result = db.count_car_model(message.text)
        recognizer = CarRecognizer(dp, bot, kiaState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Chevrolet':
        chevroletState = State.chevroletState
        result = db.count_car_model(message.text)
        recognizer = CarRecognizer(dp, bot, chevroletState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Lexus':
        lexusState = State.lexusState
        result = db.count_car_model(message.text)
        recognizer = CarRecognizer(dp, bot, lexusState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Hyundai':
        hyundaiState = State.hyundaiState
        result = db.count_car_model(message.text)
        recognizer = CarRecognizer(dp, bot, hyundaiState, message.text, result)
        await recognizer.getCar(message, state)

#carstock
@dp.message_handler(state=State.carStock)
async def process_car_stock(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await state.finish()
        await message.answer('Вы вернулись в меню!', reply_markup=kb.mainMenu)
        await State.menuState.set() 
    else:
        await rightNowAndcarStock(message, state)

#rightnow
@dp.message_handler(state=State.rightNow)
async def process_right_now(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await state.finish()
        await message.answer('Вы вернулись в меню!', reply_markup=kb.mainMenu)
        await State.menuState.set() 
    else:
        await rightNowAndcarStock(message, state)
    
@dp.message_handler(content_types=['contact'], state=State.communicationState)
async def process_communication_btn(message: types.Message, state: FSMContext):
    await bot.send_message(CHAT_ID, 'Клиент хочет связаться!')
    await bot.send_contact(CHAT_ID, message.contact.phone_number, message.contact.first_name)
    await message.answer('Отлично! Наш менеджер свяжется с вами в ближайшее время 😊', reply_markup=kb.startMenu)
    await state.finish()

@dp.message_handler(content_types=['contact'], state=State.orderState)
async def process_communication_btn(message: types.Message, state: FSMContext):
    await bot.send_message(CHAT_ID, 'Данные клиента, который интересуется покупкой!')
    await bot.send_contact(CHAT_ID, message.contact.phone_number, message.contact.first_name)
    await message.answer('Отлично! Наш менеджер свяжется с вами в ближайшее время 😊', reply_markup=kb.startMenu)
    await state.finish()

@dp.message_handler(state=State.communicationState)
async def process_communication_btn(message: types.Message, state: FSMContext):
    await message.answer(communication_msg)

@dp.message_handler(state=State.orderState)
async def process_order_btn(message: types.Message, state: FSMContext):
    await message.answer(communication_msg)

@dp.message_handler(state=State.documentState)
async def process_licensePhoto(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await state.finish()
        await message.answer('Вы переместились в стартовое меню!', reply_markup=kb.startMenu)
    elif message.text == 'Фото удостоверения 👤':
        await state.finish()
        await message.answer('Пришлите фото, чтобы мы могли рассмотреть Вашу заявку!', reply_markup=kb.cancelMenu)
        await State.certificatesPhoto.set()
    elif message.text == 'Фото прав 🆔':
        await state.finish()
        await message.answer('Пришлите фото, чтобы мы могли рассмотреть Вашу заявку!', reply_markup=kb.cancelMenu)
        await State.licensePhoto.set()

@dp.message_handler(content_types=['photo'], state=State.certificatesPhoto)
async def process_licensePhoto(message: types.Message, state: FSMContext):
    await state.finish()
    photo_id = message.photo[-1].file_id
    await bot.send_photo(CHAT_ID, photo_id, caption='Фотография удостоверения клиента')
    await message.answer('Спасибо, мы рассматриваем Вашу заявку!\nОставьте свои контакты и наш менеджер свяжется с вами в ближайшее время 🤗', reply_markup=kb.communicationMenu)
    await State.orderState.set()

@dp.message_handler(state=State.certificatesPhoto)
async def process_licensePhoto(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await state.finish()
        await message.answer('Вы переместились в стартовое меню!', reply_markup=kb.startMenu)
    else:
        await message.answer('Надо прислать фото!')

@dp.message_handler(content_types=['photo'], state=State.licensePhoto)
async def process_licensePhoto(message: types.Message, state: FSMContext):
    await state.finish()
    photo_id = message.photo[-1].file_id
    await bot.send_photo(CHAT_ID, photo_id, caption='Фотография прав клиента')
    await message.answer('Спасибо, мы рассматриваем Вашу заявку!\nОставьте свои контакты и наш менеджер свяжется с вами в ближайшее время 🤗', reply_markup=kb.communicationMenu)
    await State.orderState.set()
    
@dp.message_handler(state=State.licensePhoto)
async def process_licensePhoto(message: types.Message, state: FSMContext):
    if message.text == 'Назад ⬅️':
        await state.finish()
        await message.answer('Вы переместились в стартовое меню!', reply_markup=kb.startMenu)
    else:
        await message.answer('Надо прислать фото!')

async def rightNowAndcarStock(message: types.Message, state):
    if message.text == 'Range Rover':
        rangeState = State.rangeState
        result = db.check_car_stock(message.text)
        recognizer = CarRecognizer(dp, bot, rangeState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Toyota':
        toyotaState = State.toyotaState
        result = db.check_car_stock(message.text)
        recognizer = CarRecognizer(dp, bot, toyotaState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Mitsubishi':
        mitsubishiState = State.mitsubishiState
        result = db.check_car_stock(message.text)
        recognizer = CarRecognizer(dp, bot, mitsubishiState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Mercedes':
        mercedesState = State.mercedesState
        result = db.check_car_stock(message.text)
        recognizer = CarRecognizer(dp, bot, mercedesState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Kia':
        kiaState = State.kiaState
        result = db.check_car_stock(message.text)
        recognizer = CarRecognizer(dp, bot, kiaState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Chevrolet':
        chevroletState = State.chevroletState
        result = db.check_car_stock(message.text)
        recognizer = CarRecognizer(dp, bot, chevroletState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Lexus':
        lexusState = State.lexusState
        result = db.check_car_stock(message.text)
        recognizer = CarRecognizer(dp, bot, lexusState, message.text, result)
        await recognizer.getCar(message, state)
    elif message.text == 'Hyundai':
        hyundaiState = State.hyundaiState
        result = db.check_car_stock(message.text)
        recognizer = CarRecognizer(dp, bot, hyundaiState, message.text, result)
        await recognizer.getCar(message, state)

if __name__ == '__main__':
    from admin import dp
    executor.start_polling(dp, loop=loop, skip_updates=True)