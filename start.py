import asyncio
import os
from API.app import keep_alive
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from TelegramBot.BotCommands.start import mainpage
from TelegramBot.Cities.cities import cities
from TelegramBot.Cities.city import getCityByTitle
from TelegramBot.Callbacks.Cities.schedule import show_schedule
from TelegramBot.Callbacks.Cities.notifyMenu import notifyMenu
from TelegramBot.Callbacks.Notifications.notifyInfo import notifyInfo
from TelegramBot.Callbacks.Notifications.notifyOn import notifyOn, notifyOnMessage
from TelegramBot.Callbacks.Notifications.notifyOff import notifyOff, notifyOffMessage

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

        return await getCityByTitle(bot, message)


@bot.callback_query_handler(func=lambda query: True)
async def balance_calldata(query):
    data = query.data.split('_')
        
    if data[0] == "schedule":
        return await show_schedule(bot, query)
    
    if data[0] == "notification":
        return await notifyMenu(bot, query)
        
    if data[0] == "InfNotification":
        telegram_id = data[1]
        city_id = data[2]
        return await notifyInfo(bot, query, telegram_id, city_id)
        
    if data[0] == "OnNotification":
        city_id = data[1]
        return await notifyOn(bot, query, city_id)
        
    if data[0] == "notifyOnMessage":
        telegram_id = data[1]
        city_id = data[2]
        city_group = data[3]
        return await notifyOnMessage(bot, query, telegram_id, city_id, city_group)
        
    if data[0] == "OffNotification":
        telegram_id = data[1]
        city_id = data[2]
        return await notifyOff(bot, query, telegram_id, city_id)
        
    if data[0] == "notifyOffMessage":
        telegram_id = data[1]
        city_id = data[2]
        city_group = data[3]
        return await notifyOffMessage(bot, query, telegram_id, city_id, city_group)
        
keep_alive()
asyncio.run(bot.infinity_polling())