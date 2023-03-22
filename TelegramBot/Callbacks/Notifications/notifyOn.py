from TelegramBot.DataBase.dbRequests import getCityById, postNotifications
from telebot import types

async def notifyOn(bot, query, city_id):
    city = getCityById(city_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    row_buttons = []
    for x in range(len(city['groups'])):
        row_buttons.append(types.InlineKeyboardButton(str(x+1), callback_data = "notifyOnMessage_"+str(query.from_user.id)+"_"+str(city_id)+"_"+str(x+1)))
    markup.row(*row_buttons)    
    return await bot.send_message(query.from_user.id, "Оберіть номер черги для отримання сповіщення 🔖", reply_markup=markup, timeout=30)


async def notifyOnMessage(bot, query, telegram_id, city_id, city_group):
    statusCode = postNotifications(telegram_id, city_id, city_group)
    if statusCode == 200:
        return await bot.send_message(query.from_user.id, "🔊 Ви увімкнули сповіщення по подачі електроенергії для "+str(city_group)+"-ї групи!", timeout=30)
    return await bot.send_message(query.from_user.id, "ℹ️ Помилка! Сповіщення для даної групи заданого міста вже увімкнуто!")