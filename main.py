import telebot
from telebot import types
import Config
import DataBase

bot = telebot.TeleBot(Config.token)


# Функция на команды /start, выводит кнопки: "Поддержка", "Каталог"


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    support = types.KeyboardButton("Поддержка")
    catalog = types.KeyboardButton("Каталог")
    markup.add(support, catalog)
    bot.send_message(message.chat.id,
                     text="Нажмите на кнопку Каталог для посмотра товаров.\nНажмите на кнопку Поддержка, если возникли какие-то трудности.",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    if (message.text == "Каталог"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        doors = types.KeyboardButton("Двери")
        drips = types.KeyboardButton("Дриптипы")
        basket = types.KeyboardButton("Корзина")
        back = types.KeyboardButton("Назад")
        markup.add(doors, drips, basket, back)
        bot.send_message(message.chat.id, text="Выберете интересующий вас товар.", reply_markup=markup)

    elif message.text == "Двери":
        markup = types.InlineKeyboardMarkup(row_width=1)
        door1 = types.InlineKeyboardButton("Dot Aio mini", callback_data="door1")
        door2 = types.InlineKeyboardButton("Dot Aio V2", callback_data="door2")
        markup.add(door1, door2)
        bot.send_message(message.chat.id, text="Выберете интересующюю дверь:", reply_markup=markup)

    elif message.text == "Дриптипы":
        markup = types.InlineKeyboardMarkup(row_width=1)
        drip1 = types.InlineKeyboardButton("510 длинный", callback_data="drip1")
        drip2 = types.InlineKeyboardButton("510 стандарт", callback_data="drip2")
        markup.add(drip1, drip2)
        bot.send_message(message.chat.id, text="Выберете интересующий дриптип:", reply_markup=markup)

    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        support = types.KeyboardButton("Поддержка")
        catalog = types.KeyboardButton("Каталог")
        markup.add(support, catalog)
        bot.send_message(message.chat.id,
                         text="Главная",
                         reply_markup=markup)
    elif message.text == "Корзина":
        userId = message.chat.username
        Cart = DataBase.GetCart(userId)
        for i, (item, quantity, price) in enumerate(Cart):
            markup = types.InlineKeyboardMarkup(row_width=2)
            dataBack1 = f"plus{item}"
            dataBack2 = f"minus{item}"
            plus = types.InlineKeyboardButton("+", callback_data=dataBack1)
            minus = types.InlineKeyboardButton("-", callback_data=dataBack2)
            markup.add(plus, minus)

            text = f"{item}\nКоличество: {quantity}\nСтоимость: {price}руб."
            bot.send_message(message.chat.id, text, reply_markup=markup)



#хууууууууууууууууууй
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "door1":
        markup = types.InlineKeyboardMarkup(row_width=1)
        putbasket = types.InlineKeyboardButton("Добавить в корзину", callback_data="Dot Aio mini")
        markup.add(putbasket)
        bot.send_message(call.message.chat.id, text="Дверь: Dot Aio mini\nЦена: 1500 руб.", reply_markup=markup)

    elif call.data == "door2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        putbasket = types.InlineKeyboardButton("Добавить в корзину", callback_data="Dot Aio V2")
        markup.add(putbasket)
        bot.send_message(call.message.chat.id, text="Дверь: Dot Aio V2\nЦена: 1500 руб.", reply_markup=markup)

    elif call.data == "drip1":
        markup = types.InlineKeyboardMarkup(row_width=1)
        putbasket = types.InlineKeyboardButton("Добавить в корзину", callback_data="510 длинный")
        markup.add(putbasket)
        bot.send_message(call.message.chat.id, text="Дриптип: 510 длинный\nЦена: 300 руб.", reply_markup=markup)

    elif call.data == "drip2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        putbasket = types.InlineKeyboardButton("Добавить в корзину", callback_data="510 стандарт")
        markup.add(putbasket)
        bot.send_message(call.message.chat.id, text="Дриптип: 510 стандарт\nЦена: 300 руб.", reply_markup=markup)


    elif call.data == "Dot Aio mini":
        userId = call.message.chat.username
        DataBase.CheckCustomer(userId)
        DataBase.OrderCreator(userId, call.data)
        bot.send_message(call.message.chat.id, "Товар добавлен в корзину")


    elif call.data == "Dot Aio V2":
        userId = call.message.chat.username
        DataBase.CheckCustomer(userId)
        DataBase.OrderCreator(userId, call.data)
        bot.send_message(call.message.chat.id, text="Товар добавлен в корзину")

    elif call.data == "510 длинный":
        userId = call.message.chat.username
        DataBase.CheckCustomer(userId)
        DataBase.OrderCreator(userId, call.data)
        bot.send_message(call.message.chat.id, text="Товар добавлен в корзину")


    elif call.data == "510 стандарт":
        userId = call.message.chat.username
        DataBase.CheckCustomer(userId)
        DataBase.OrderCreator(userId, call.data)
        bot.send_message(call.message.chat.id, text="Товар добавлен в корзину")


    # elif call.data =="plusDot Aio mini" or call.data == "minusDot Aio mini":
    #     if call.data =="plusDot Aio mini":
    #


bot.polling(none_stop=True)
