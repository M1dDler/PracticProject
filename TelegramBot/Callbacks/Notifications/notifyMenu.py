from TelegramBot.dbRequests import getCityById
from telebot import types

async def notifyMenu(bot, query):
    city_id  = query.data.split("_") 
    city_id = city_id[1]
    city = getCityById(city_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    show_notifications_btn = types.InlineKeyboardButton("🔈 Мої активні сповіщення", callback_data = "InfNotification_"+str(query.from_user.id)+"_"+str(city_id))
    on_btn = types.InlineKeyboardButton("🔊 Увімкнути  сповіщення для м."+city['city_name'], callback_data = "OnNotification_"+str(city_id))
    off_btn = types.InlineKeyboardButton("🔇 Вимкнути  сповіщення для м."+city['city_name'], callback_data="OffNotification_"+str(query.from_user.id)+"_"+str(city_id))
    markup.add(show_notifications_btn, on_btn, off_btn)
    return await bot.send_message(query.from_user.id, "Оберіть те, що вас цікавить ⤵️", reply_markup=markup)