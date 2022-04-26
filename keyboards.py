from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

#cancel
cancel_btn = KeyboardButton('Назад ⬅️')
cancelMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(cancel_btn)

#start menu
menu_btn = KeyboardButton('Меню 🚘')
about_btn = KeyboardButton('О нас 💬')
contact_btn = KeyboardButton('Контакты 📞')
communication_btn = KeyboardButton('Связь с менеджером 📲')
startMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(menu_btn).row(about_btn).row(contact_btn).row(communication_btn)

#main menu
catalog_btn = KeyboardButton('Каталог машин 🚛')
order_car_rn_btn = KeyboardButton('Заказать машину прямо сейчас 🚀')
cars_stock_btn = KeyboardButton('Машины в наличии 🚨')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(catalog_btn).row(order_car_rn_btn).row(cars_stock_btn).row(communication_btn, cancel_btn)

#model menu
range_btn = KeyboardButton('Range Rover')
toyota_btn = KeyboardButton('Toyota')
kia_btn = KeyboardButton('Kia')
lexus_btn = KeyboardButton('Lexus')
hyundai_btn = KeyboardButton('Hyundai')
mercedes_btn = KeyboardButton('Mercedes')
chevrolet_btn = KeyboardButton('Chevrolet')
mitsubishi_btn = KeyboardButton('Mitsubishi')
modelMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(range_btn, toyota_btn, kia_btn).row(lexus_btn, hyundai_btn).row(mercedes_btn, chevrolet_btn, mitsubishi_btn).row(cancel_btn)

#contact menu
instagram_btn = InlineKeyboardButton('Инстаграм 📸', url='https://www.instagram.com/')
site_btn = InlineKeyboardButton('Сайт 🖥', url='https://rentacars.kz/')
contactMenu = InlineKeyboardMarkup().row(instagram_btn).row(site_btn)

#communication menu
user_contact_btn = KeyboardButton('Оставить свой контакт 📲', request_contact=True)
communicationMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(user_contact_btn)

#order 
order_car = InlineKeyboardButton('Заказать 📞', callback_data=f'order_car')
orderMenu = InlineKeyboardMarkup().row(order_car)

#orderProcess
certificates_photo = KeyboardButton('Фото удостоверения 👤')
license_photo = KeyboardButton('Фото прав 🆔')
licenseMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(certificates_photo, license_photo).row(cancel_btn)

#admin menu
car_stock = KeyboardButton('Машины в наличии 🎯')
add_car = KeyboardButton('Добавить машину 🚘')
to_start_menu = KeyboardButton('В стартовое меню ⬅️')
adminMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(car_stock).row(to_start_menu)

#car menu
orderCar = InlineKeyboardButton('Заказать 📞', callback_data=f'OrderCar')
nextCar = InlineKeyboardButton('Следующая 🏎', callback_data=f'NextCar')
carMenu = InlineKeyboardMarkup().row(nextCar).row(orderCar)

#stock menu
stockCar = InlineKeyboardButton('В наличии ✅', callback_data='stockCar')
outOfStockCar= InlineKeyboardButton('Нет в наличии ❌', callback_data='outOfStockCar')
stockMenu = InlineKeyboardMarkup().row(stockCar, outOfStockCar).row(nextCar)

#date menu
firstDate = KeyboardButton('25 суток-месяц') 
secondDate = KeyboardButton('15-24 суток') 
thirdDate = KeyboardButton('7-14 суток')
fourthDate = KeyboardButton('3-6 суток')
fifthDate = KeyboardButton('1-2 суток')
dateMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(firstDate, secondDate).row(thirdDate, fourthDate).row(fifthDate).row(cancel_btn)

#buy menu
buyBtn = InlineKeyboardButton('Оплатить 💳', callback_data='buyBtn')
buyMenu = InlineKeyboardMarkup().row(buyBtn)