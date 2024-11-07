
import aiogram.filters
from telebot.types import InlineKeyboardButton
import telebot

import Config

import Config
import DataBase
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F
from aiogram.types import FSInputFile, InputMediaPhoto

bot = Bot(token=Config.token)
dp = Dispatcher()
Support = "@queenstealer"
router = Router()

dp.include_router(router)
#Функция на команды /start, выводит кнопки: "Поддержка", "Каталог"

# bot1 = telebot.TeleBot(Config.token)

# @bot1.message_handler(commands=['start'])
# def send_welcome(message):
#     user_id = message.from_user.id  # Получаем user_id
#     print(user_id)
#     bot1.reply_to(message,"'Ns gbljh'  - Расшифруй")
#
# bot1.polling()

async def set_bot_commands():
    commands = [
        types.BotCommand(command="/start", description="Начать заново"),
        types.BotCommand(command="/restart", description="Перезапустить бота"),
    ]
    await bot.set_my_commands(commands)

@dp.message(Command(commands = ['start','restart']))
async def start(message: types.Message):
    markup = ReplyKeyboardBuilder()
    catalog = types.KeyboardButton(text = "Каталог")
    markup.add( catalog)
    await message.answer(
                     text="Нажмите на кнопку Каталог для посмотра товаров.",
                     reply_markup=markup.as_markup(resize_keyboard=True)
    )


@dp.message(F.text.in_({"Каталог","Двери","Дриптипы","Назад","Корзина","Корзина","Заказать"}))
async def text(message: types.Message):
    match message.text:

        case "Каталог" :
            markup = ReplyKeyboardBuilder()
            doors = types.KeyboardButton(text = "Двери")
            drips = types.KeyboardButton(text = "Дриптипы")
            basket = types.KeyboardButton(text = "Корзина")
            # back = types.KeyboardButton("Назад")
            markup.add(doors, drips, basket)
            await message.answer(text="Выберете интересующий вас товар.",
                                 reply_markup=markup.as_markup(resize_keyboard=True)
                                 )


        case "Двери":
            markup = InlineKeyboardBuilder()
            door1 = types.InlineKeyboardButton(text = "Dot Aio mini", callback_data="door1")
            door2 = types.InlineKeyboardButton(text = "Dot Aio V2", callback_data="door2")
            markup.add(door1, door2)
            await message.answer(text="Выберете интересующюю дверь:",
                                 reply_markup=markup.as_markup(resize_keyboard=True)
                                 )

        case "Дриптипы":
            markup = InlineKeyboardBuilder()
            drip1 = types.InlineKeyboardButton(text = "510 длинный", callback_data="drip1")
            drip2 = types.InlineKeyboardButton(text = "510 стандарт", callback_data="drip2")
            markup.add(drip1, drip2)
            await message.answer(text="Выберете интересующий дриптип:",
                                 reply_markup=markup.as_markup(resize_keyboard=True)
                                 )

        case "Назад":
            markup = ReplyKeyboardBuilder()
            doors = types.KeyboardButton(text="Двери")
            drips = types.KeyboardButton(text="Дриптипы")
            basket = types.KeyboardButton(text="Корзина")
            markup.add(doors, drips, basket)
            await message.answer(text="Выберете интересующий вас товар.",
                                 reply_markup=markup.as_markup(resize_keyboard=True)
                                 )

        case "Заказать":
            # username = "queenstealer"
            # user = await bot.get_chat(username)
            userId = message.from_user.username
            Cart = await DataBase.GetCart(userId)
            await DataBase.DeleteCart(userId)
            Order = Config.order
            await bot.send_message(chat_id=Order,text = userId)
            for i, (item, quantity, price) in enumerate(Cart):
                text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                await bot.send_message(chat_id=Order,text ="@"+text)
            await message.answer(text = "Заказ отправлен нашему работнику, в течении 2 часов он напишет вам, по поводу заказа.")


        case "Корзина":
            userId = message.from_user.username
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await message.answer("Корзина пуста")

            else:
                markup = ReplyKeyboardBuilder()
                back = types.KeyboardButton(text="Назад")
                order = types.KeyboardButton(text="Заказать")
                markup.add(back, order)
                await message.answer("Если собираетесь сделать заказ, нажмите на соответствующую кнопку на панели",
                                     reply_markup=markup.as_markup(resize_keyboard=True))

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text = "+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text = "-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await message.answer(text, reply_markup=markup.as_markup())




@dp.callback_query(F.data.in_({"door1", "door2", "drip1", "drip2","Dot Aio mini","Dot Aio V2","510 длинный","510 стандарт",
                               "plusDot Aio mini","minusDot Aio mini","plusDot Aio V2","minusDot Aio V2","plus510 длинный",
                               "minus510 длинный","plus510 стандарт","minus510 стандарт",}) )
async def CallData(call: types.CallbackQuery):
    match call.data:
        case "door1":

            markup = InlineKeyboardBuilder()
            markup.add(types.InlineKeyboardButton(text = "Добавить в корзину", callback_data="Dot Aio mini"))
            photo =FSInputFile(Config.Photo["Door1"])
            await call.message.answer_photo(photo = photo)
            await call.message.answer(text = "Дверь: Dot Aio mini\nЦена: 1500 руб.", reply_markup=markup.as_markup())

        case "door2":

            markup = InlineKeyboardBuilder()
            markup.add(types.InlineKeyboardButton(text = "Добавить в корзину", callback_data="Dot Aio V2"))
            photo1 = InputMediaPhoto(media = FSInputFile(Config.Photo["Door2.1"]))
            photo2 = InputMediaPhoto(media = FSInputFile(Config.Photo["Door2.2"]))
            await call.message.answer_media_group(media = [photo1, photo2])
            await call.message.answer(text = "Дверь: Dot Aio V2\nЦена: 1500 руб.",reply_markup=markup.as_markup())



        case "drip1":

            markup = InlineKeyboardBuilder()
            markup.add(types.InlineKeyboardButton(text = "Добавить в корзину", callback_data="510 длинный"))
            photo = FSInputFile(Config.Photo["Drip2"])
            await call.message.answer_photo(photo = photo)
            await call.message.answer(text = "Дриптип: 510 длинный\nЦена: 300 руб.", reply_markup=markup.as_markup())

        case "drip2":
            markup = InlineKeyboardBuilder()
            markup.add(types.InlineKeyboardButton(text ="Добавить в корзину", callback_data="510 стандарт"))
            photo = FSInputFile(Config.Photo["Drip1"])
            await call.message.answer_photo(photo = photo)
            await  call.message.answer(text = "Дриптип: 510 стандарт\nЦена: 300 руб.", reply_markup=markup.as_markup())


        case "Dot Aio mini":
            userId = call.from_user.username
            await DataBase.CheckCustomer(userId)
            await DataBase.OrderCreator(userId, call.data)
            await call.message.answer(text = "Товар добавлен в корзину")


        case "Dot Aio V2":
            userId = call.from_user.username
            await DataBase.CheckCustomer(userId)
            await DataBase.OrderCreator(userId, call.data)
            await call.message.answer(text = "Товар добавлен в корзину")

        case "510 длинный":
            userId = call.from_user.username
            await DataBase.CheckCustomer(userId)
            await DataBase.OrderCreator(userId, call.data)
            await call.message.answer(text = "Товар добавлен в корзину")


        case "510 стандарт":
            userId = call.from_user.username
            await DataBase.CheckCustomer(userId)
            await DataBase.OrderCreator(userId, call.data)
            await call.message.answer(text = "Товар добавлен в корзину")


        case "plusDot Aio mini":

            userId = call.message.chat.username
            await DataBase.Plus(userId, call.data)
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await call.message.answer(text = "Корзина пуста")

            else:

                await call.message.answer(text = "Корзина обновлена")

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text="+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text="-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await call.message.answer(text, reply_markup=markup.as_markup())


        case "minusDot Aio mini":

            userId = call.message.chat.username
            await DataBase.Minus(userId, call.data)
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await bot.send_message(call.message.chat.id, "Корзина пуста")
            else:

                await bot.send_message(call.message.chat.id, "Корзина обновлена")

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text="+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text="-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await call.message.answer(text, reply_markup=markup.as_markup())


        case "plusDot Aio V2":

            userId = call.message.chat.username
            await DataBase.Plus(userId, call.data)
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await bot.send_message(call.message.chat.id, "Корзина пуста")

            else:

                await bot.send_message(call.message.chat.id, "Корзина обновлена")

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text="+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text="-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await call.message.answer(text, reply_markup=markup.as_markup())

        case "minusDot Aio V2":

            userId = call.message.chat.username
            await DataBase.Minus(userId, call.data)
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await bot.send_message(call.message.chat.id, "Корзина пуста")

            else:

                await bot.send_message(call.message.chat.id, "Корзина обновлена")

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text="+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text="-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await call.message.answer(text, reply_markup=markup.as_markup())


        case "plus510 длинный":

            userId = call.message.chat.username
            await DataBase.Plus(userId, call.data)
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await bot.send_message(call.message.chat.id, "Корзина пуста")

            else:

                await bot.send_message(call.message.chat.id, "Корзина обновлена")

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text="+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text="-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await call.message.answer(text, reply_markup=markup.as_markup())

        case "minus510 длинный":

            userId = call.message.chat.username
            await DataBase.Minus(userId, call.data)
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await bot.send_message(call.message.chat.id, "Корзина пуста")

            else:

                await bot.send_message(call.message.chat.id, "Корзина обновлена")

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text="+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text="-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await call.message.answer(text, reply_markup=markup.as_markup())


        case "plus510 стандарт":
            userId = call.message.chat.username
            await DataBase.Plus(userId, call.data)
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await bot.send_message(call.message.chat.id, "Корзина пуста")

            else:

                await bot.send_message(call.message.chat.id, "Корзина обновлена")

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text="+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text="-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await call.message.answer(text, reply_markup=markup.as_markup())

        case "minus510 стандарт":

            userId = call.message.chat.username
            await DataBase.Minus(userId, call.data)
            Cart = await DataBase.GetCart(userId)

            if Cart == False:

                await bot.send_message(call.message.chat.id, "Корзина пуста")

            else:

                await bot.send_message(call.message.chat.id, "Корзина обновлена")

                for i, (item, quantity, price) in enumerate(Cart):
                    markup = InlineKeyboardBuilder()
                    dataBack1 = f"plus{item}"
                    dataBack2 = f"minus{item}"
                    plus = types.InlineKeyboardButton(text="+", callback_data=dataBack1)
                    minus = types.InlineKeyboardButton(text="-", callback_data=dataBack2)
                    markup.add(plus, minus)
                    markup.adjust(2)

                    text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
                    await call.message.answer(text, reply_markup=markup.as_markup())



async def main():
    await set_bot_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    dp.run_polling(bot)
