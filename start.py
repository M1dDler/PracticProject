import asyncio
import os
from API.app import keep_alive
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from TelegramPages.mainpage import *
from TelegramPages.cities import *
from TelegramRequests.dataRequests import *

load_dotenv()
token = os.getenv("BOTTOKEN")
bot = AsyncTeleBot(token)

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    if message.content_type == 'text':
        if not message.entities == None:
            if message.entities[0].type == 'bot_command':
                
                if message.text == '/start':
                    return await mainpage(bot, message)
            return
        
        if message.text == 'Список населених пунктів 🏘':
            return await cities(bot, message)

        return await findCityByTitle(bot, message)


@bot.callback_query_handler(func=lambda query: True)
async def balance_calldata(query):
    data = query.data.split('_')
        
    if data[0] == "schedule":
        await show_schedule_on(bot, query)
        await show_schedule_maybe(bot, query)
        return await show_schedule_off(bot, query)
    
    if data[0] == "notification":
        city_id  = query.data.split("_") 
        city_id = city_id[1]
        city = getCityById(city_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        show_notifications_btn = types.InlineKeyboardButton("🔈 Мої активні сповіщення", callback_data = "InfNotification_"+str(query.from_user.id)+"_"+str(city_id))
        on_btn = types.InlineKeyboardButton("🔊 Увімкнути  сповіщення для м."+city['city_name'], callback_data = "OnNotification_"+str(city_id))
        off_btn = types.InlineKeyboardButton("🔇 Вимкнути  сповіщення для м."+city['city_name'], callback_data="OffNotification_"+str(query.from_user.id)+"_"+str(city_id))
        
        markup.add(show_notifications_btn, on_btn, off_btn)
        
        return await bot.send_message(query.from_user.id, "Оберіть те, що вас цікавить ⤵️", reply_markup=markup)
        
    if data[0] == "InfNotification":
        city = getCityById(data[2])    
        notifications = getNotifications(data[1], data[2])
        if len(notifications) == 0:
            return await bot.send_message(query.from_user.id, "ℹ️ Поки що немає жодних активних сповіщень по місту " + city['city_name'] + ".")
        text = "<b>Список активних сповіщень для м." + city['city_name'] + "⤵️\n\n</b>"+"\n".join(str('📌 Черга - №'+str(x['city_group'])) for x in notifications)
        return await bot.send_message(query.from_user.id, text, parse_mode='HTML')
        
    if data[0] == "OnNotification":
        city_id = data[1]
        city = getCityById(city_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        row_buttons = []
        for x in range(len(city['groups'])):
            row_buttons.append(types.InlineKeyboardButton(str(x+1), callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_"+str(x+1)))
            
        markup.row(*row_buttons)
        
        return await bot.send_message(query.from_user.id, "Оберіть номер черги для отримання сповіщення 🔖", reply_markup=markup, timeout=30)
        
    if data[0] == "group":
        telegram_id = data[1]
        city_id = data[2]
        city_group = data[3]
        statusCode = postNotifications(telegram_id, city_id, city_group)
        if statusCode == 200:
            return await bot.send_message(query.from_user.id, "🔊 Ви увімкнули сповіщення по подачі електроенергії для "+str(city_group)+"-ї групи!", timeout=30)
        return await bot.send_message(query.from_user.id, "ℹ️ Помилка! Сповіщення для даної групи заданого міста вже увімкнуто!")
    
    if data[0] == "OffNotification":
        city = getCityById(data[2])
        groups = (len(city['groups']))
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        row_buttons = []
        for x in range(groups):
            row_buttons.append(types.InlineKeyboardButton(str(x+1), callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_"+str(x+1))))
        
        markup.row(*row_buttons)
        
        return await bot.send_message(query.from_user.id, "Оберіть чергу увімкнення/вимкнення електроенергії м."+city['city_name']+
                                   " для виключення сповіщення 🔖", reply_markup=markup)
        
    if data[0] == "delgroup":
        statusCode = deleteNotifications(data[1], data[2], data[3])
        if statusCode == 200:
            return await bot.send_message(query.from_user.id, "🔇 Ви вимкнули сповіщення по подачі електроенергії для "+data[3]+"-ї групи!", timeout=30)
        return await bot.send_message(query.from_user.id, "ℹ️ Активних сповіщень по даній черзі не виявлено!", timeout=30) 
        
keep_alive()
asyncio.run(bot.infinity_polling())