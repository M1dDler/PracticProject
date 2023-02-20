from telebot import types
from telebot.async_telebot import AsyncTeleBot

async def mainpage(bot, message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard = True)
    cities_btn = types.KeyboardButton("Список населених пунктів 🏘")
    markup.add(cities_btn)
    await bot.send_message(message.from_user.id, "Введіть свій населений пункт для отримання інформації про подачу електроенергії 😇\n", reply_markup=markup, timeout=30)
    