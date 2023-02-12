import telebot
import asyncio
import os
import json
from API.api import keep_alive
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from TelegramPages.mainpage import *
from TelegramPages.cities import *

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
        
    if (query.data == "show_schedule_call"):
        return
    
    if (query.data == "show_notification_call"):
        return
    
    

keep_alive()
asyncio.run(bot.infinity_polling())