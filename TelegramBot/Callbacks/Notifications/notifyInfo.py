from TelegramBot.DataBase.dbRequests import getCityById, getNotifications

async def notifyInfo(bot, query, telegram_id, city_id):
    city = getCityById(city_id)    
    notifications = getNotifications(telegram_id, city_id)
    if len(notifications) == 0:
        return await bot.send_message(query.from_user.id, "ℹ️ Поки що немає жодних активних сповіщень по місту " + city['city_name'] + ".")
    text = "<b>Список активних сповіщень для м." + city['city_name'] + "⤵️\n\n</b>"+"\n".join(str('📌 Черга - №'+str(x['city_group'])) for x in notifications)
    return await bot.send_message(query.from_user.id, text, parse_mode='HTML')
    