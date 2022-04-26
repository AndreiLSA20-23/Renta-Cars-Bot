import re
from aiogram import types
from aiogram.types.message import ContentType
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ParseMode
import keyboards as kb
from config import *
from utils import *
from messages import *\


class BuyCar:
    def __init__(self, dp, bot, result, CarID):
        self.dp = dp
        self.bot = bot
        self.result = result
        self.CarID = CarID

    async def getDate(self):
        print(self.result)
        @self.dp.message_handler(state=State.buyState)
        async def process_buyState(message: types.Message, state: FSMContext):  
            if message.text == 'Назад ⬅️':
                await state.finish()
                await message.answer('Вы вернулись в меню марок!', reply_markup=kb.modelMenu)
                await State.modelCar.set()
            elif message.text == '25 суток-месяц':
                firstPrice = re.split('в|/',self.result[self.CarID][4])[0].replace('тг. ', '')
                amount = int(firstPrice) * 100
                await message.answer('Теперь, надо оплатить по кнопке ниже ⬇️', reply_markup=kb.buyMenu, parse_mode=ParseMode.MARKDOWN)
                await self.getInvoice(amount, message, state)
            elif message.text == '15-24 суток':
                secondPrice = re.split('в|/',self.result[self.CarID][4])[1].replace('сутки25 суток-месяц ', '').replace('тг. ', '')
                amount = int(secondPrice) * 100
                await message.answer('Теперь, надо оплатить по кнопке ниже ⬇️', reply_markup=kb.buyMenu, parse_mode=ParseMode.MARKDOWN)
                await self.getInvoice(amount, message, state) 
            elif message.text == '7-14 суток':
                thirdPrice = re.split('в|/',self.result[self.CarID][4])[2].replace('сутки15-24 суток ', '').replace('тг. ', '')
                amount = int(thirdPrice) * 100
                await message.answer('Теперь, надо оплатить по кнопке ниже ⬇️', reply_markup=kb.buyMenu, parse_mode=ParseMode.MARKDOWN) 
                await self.getInvoice(amount, message, state)
            elif message.text == '3-6 суток':
                fourthPrice = re.split('в|/',self.result[self.CarID][4])[3].replace('сутки7-14 суток ', '').replace('тг. ', '')
                amount = int(fourthPrice) * 100
                await message.answer('Теперь, надо оплатить по кнопке ниже ⬇️', reply_markup=kb.buyMenu, parse_mode=ParseMode.MARKDOWN) 
                await self.getInvoice(amount, message, state) 
            elif message.text == '1-2 суток':
                fifthPrice = re.split('в|/',self.result[self.CarID][4])[4].replace('сутки3-6 суток ', '') .replace('тг. ', '')
                amount = int(fifthPrice) * 100
                await message.answer('Теперь, надо оплатить по кнопке ниже ⬇️', reply_markup=kb.buyMenu, parse_mode=ParseMode.MARKDOWN)  
                await self.getInvoice(amount, message, state)
            else:
                await message.answer('Вы хотите вернуться назад? Нажмите на кнопку ниже!')   

    async def getInvoice(self, amount, message, state):   
        print(carName) 
        carName = self.result[self.CarID][0]
        try:
            PRICE = types.LabeledPrice(label=carName, amount=amount)
        except:
            pass
        PICKUP_SHIPPING_OPTION = types.ShippingOption(id='pickup', title='Самовывоз')
        PICKUP_SHIPPING_OPTION.add((types.LabeledPrice('Pickup', 0)))

        @self.dp.callback_query_handler(text='buyBtn', state=State.buyState)
        async def process_order_callback(call: types.CallbackQuery):
            print(PRICE)
            await state.finish()
            await self.bot.send_invoice(call.message.chat.id, 
            title=carName,
            description=carName,
            provider_token=PAYMENT_TOKEN,
            currency='KZT',
            photo_url='',
            photo_height=512,
            photo_width=512,
            photo_size=512,
            need_email=True,
            need_phone_number=True,
            is_flexible=True,
            prices=[PRICE],
            start_parameter='example',
            payload='some_invoices') 

            await message.answer('Также для отмены заказа, напишете /cancel', reply_markup=ReplyKeyboardRemove())

            @self.dp.shipping_query_handler(lambda query: True)
            async def process_shipping_query(shipping_query: types.ShippingQuery):
                if shipping_query.shipping_address.country_code != 'KZ':
                    return await self.bot.answer_shipping_query(shipping_query.id,
                    ok=False, error_message=country_error)
                if shipping_query.shipping_address.country_code == 'KZ':
                    if shipping_query.shipping_address.city == 'Нур-Султан' or 'Алмата':
                        shipping_options = [PICKUP_SHIPPING_OPTION]
                await self.bot.answer_shipping_query(shipping_query.id, 
                ok=True, shipping_options=shipping_options)

            @self.dp.pre_checkout_query_handler(lambda query: True)
            async def process_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
                if hasattr(pre_checkout_query.order_info, 'email'):
                    return await self.bot.answer_pre_checkout_query(
                        pre_checkout_query.id,
                        ok=False,
                        error_message=wrong_email)
                await self.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

            @self.dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
            async def process_succesful_payment(message: types.Message):
                await self.bot.send_message(message.chat.id, successful_payment.format(
                total_amount=message.successful_payment.total_amount // 100,
                currency=message.successful_payment.currency))
                await message.answer('Для окончания заказа, надо прислать лицензию!', reply_markup=kb.licenseMenu)
                await self.bot.send_message(CHAT_ID, f'*Клиент интересуется {self.result[self.CarID][0]}*', parse_mode=ParseMode.MARKDOWN)
                await State.documentState.set() 
                await message.delete()
            