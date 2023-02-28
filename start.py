import telebot
import asyncio
import os
from API.api import keep_alive
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
        text = "<b>Список активних сповіщень для м." + city['city_name'] + "⤵️\n\n</b>"+"\n".join(str('📌 Черга - №'+str(x['city_group'])) for x in notifications)
        return await bot.send_message(query.from_user.id, text, parse_mode='HTML')
        
    if data[0] == "OnNotification":
        city_id = data[1]
        city = getCityById(city_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        one_btn = types.InlineKeyboardButton("1️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_1")
        two_btn = types.InlineKeyboardButton("2️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_2")
        three_btn = types.InlineKeyboardButton("3️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_3")
        four_btn = types.InlineKeyboardButton("4️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_4")
        five_btn = types.InlineKeyboardButton("5️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_5")
        six_btn = types.InlineKeyboardButton("6️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_6")
        seven_btn = types.InlineKeyboardButton("7️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_7")
        eight_btn = types.InlineKeyboardButton("8️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_8")
        nine_btn = types.InlineKeyboardButton("9️⃣", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_9")
        ten_btn = types.InlineKeyboardButton("🔟", callback_data = "group_"+str(query.from_user.id)+"_"+str(city_id)+"_10")
        
        list_buttons = [one_btn, two_btn, three_btn, four_btn, five_btn, six_btn, seven_btn, eight_btn, nine_btn, ten_btn]
        row_buttons = []
        for x in range(len(city['groups'])):
            row_buttons.append(list_buttons[x])
            
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
        one_btn = types.InlineKeyboardButton("1️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_1"))
        two_btn = types.InlineKeyboardButton("2️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_2"))
        three_btn = types.InlineKeyboardButton("3️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_3"))
        four_btn = types.InlineKeyboardButton("4️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_4"))
        five_btn = types.InlineKeyboardButton("5️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_5"))
        six_btn = types.InlineKeyboardButton("6️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_6"))
        seven_btn = types.InlineKeyboardButton("7️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_7"))
        eight_btn = types.InlineKeyboardButton("8️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_8"))
        nine_btn = types.InlineKeyboardButton("9️⃣", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_9"))
        ten_btn = types.InlineKeyboardButton("🔟", callback_data = "delgroup_"+str(query.from_user.id)+"_"+str(data[2]+"_10"))
        list_buttons = [one_btn, two_btn, three_btn, four_btn, five_btn, six_btn, seven_btn, eight_btn, nine_btn, ten_btn]
        row_buttons = []
        for x in range(groups):
            row_buttons.append(list_buttons[x])
        
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