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
        return await notification(bot, query)
    
    if data[0] == "group":
        telegram_id = data[1]
        city_id = data[2]
        city_group = data[3]
        statusCode = postNotifications(telegram_id, city_id, city_group)
        if statusCode == 200:
            return await bot.send_message(query.from_user.id, "🔊 Ви включили сповіщення по подачі електроенергії для "+str(city_group)+"-ї групи!", timeout=30)
        return await bot.send_message(query.from_user.id, "ℹ️ Помилка! Сповіщення для даної групи заданого міста вже увімкнуто!")
    
    if data[0] == "delete" and data[1] == "group":
        telegram_id = data[2]
        statusCode = deleteNotifications(telegram_id)
        if statusCode == 200:
            return await bot.send_message(query.from_user.id, "🔇 Всі наявні сповіщення вимкнуто!", timeout=30)
        return await bot.send_message(query.from_user.id, "ℹ️ Активних сповіщень не виявлено!", timeout=30)  
        
keep_alive()
asyncio.run(bot.infinity_polling())