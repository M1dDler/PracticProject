from TelegramBot.DataBase.dbRequests import getCityById, deleteNotifications
from telebot import types

async def notifyOff(bot, query, telegram_id, city_id):
    city = getCityById(city_id)
    groups = (len(city['groups']))    
    markup = types.InlineKeyboardMarkup(row_width=1)
    row_buttons = []
    for x in range(groups):
        row_buttons.append(types.InlineKeyboardButton(str(x+1), callback_data = "notifyOffMessage_"+str(telegram_id)+"_"+str(city_id)+"_"+str(x+1)))
    markup.row(*row_buttons)    
    return await bot.send_message(query.from_user.id, "Оберіть чергу увімкнення/вимкнення електроенергії м."+city['city_name']+
                                   " для виключення сповіщення 🔖", reply_markup=markup)
    
    
async def notifyOffMessage(bot, query, telegram_id, city_id, city_group):
    statusCode = deleteNotifications(telegram_id, city_id, city_group)
    if statusCode == 200:
        return await bot.send_message(query.from_user.id, "🔇 Ви вимкнули сповіщення по подачі електроенергії для "+city_group+"-ї групи!", timeout=30)
    return await bot.send_message(query.from_user.id, "ℹ️ Активних сповіщень по даній черзі не виявлено!", timeout=30) 