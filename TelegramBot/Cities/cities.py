from TelegramBot.DataBase.dbRequests import getCities

async def cities(bot, message):
    cities = getCities()
    
    if len(cities) == 0:
        return await bot.send_message(message.from_user.id, "В списку немає жодного населеного пункту! 😣", timeout=30)
    
    text_message = "<b>Інформація про подачу електроенергії доступна для таких міст:</b> ⤵️\n\n" + "\n".join(str('📌 '+x['city_name']) for x in cities)
    await bot.send_message(chat_id=message.from_user.id, text=text_message +'\n\n'+
                           'Для відображення детальної інформації введіть в чат назву населеного пункту ✏️'
                           ,parse_mode='HTML', timeout=30)