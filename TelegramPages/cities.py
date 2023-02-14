import datetime
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from TelegramRequests.dataRequests import *

async def cities(bot, message):
    cities = getCities()
    
    text_message = "<b>Інформація про подачу електроенергії доступна для таких міст:</b> ⤵️\n\n" + "\n".join(str('📌 '+x['city_name']) for x in cities)
    await bot.send_message(chat_id=message.from_user.id, text=text_message +'\n\n'+
                           'Для відображення детальної інформації введіть в чат назву населеного пункту ✏️'
                           ,parse_mode='HTML')
    
    
async def findCityByTitle(bot, message):
    city = getCityByTitle(message)
    
    if city == None:
        return await bot.send_message (message.from_user.id, 'Вказаного вами населеного пункту, не знайдено!')
    
    current_time = str(datetime.datetime.now().time())
    time_to_find = current_time.split(":")
    
    light_status_groups = []
    
    for group in city['groups']:
        for x in group['schedule']:
            if str(x['time']) == str(time_to_find[0]):
                status = ""
                if str(x['light']) == 'on':
                    status = 'Увімкнено ✅'
                elif str(x['light']) == 'maybe':
                    status = 'Можливе включення або виключення ⚠️'
                elif str(x['light']) == 'off':
                    status = 'Вимкнено ❌'
                light_status_groups.append(status)
            
    markup = types.InlineKeyboardMarkup(row_width=2)
    show_schedule_btn = types.InlineKeyboardButton("⏱ Розклад", callback_data = "schedule_"+str(city['city_id']))
    show_notification_btn = types.InlineKeyboardButton("🔊 Сповіщення", callback_data = "notification_"+str(city['city_id']))
    markup.add(show_schedule_btn, show_notification_btn)
            
    text_message = ("📋 Інформація щодо подачі електроенергії у м."+city['city_name']+":\n"+
                    "⚡️ Кількість черг: - "+str(len(city['groups'])) +"\n"+
                    "❕ Станом на "+time_to_find[0]+":"+time_to_find[1]+", статус електромережі в \n"+"\n".join('=== '+str(light_status_groups.index(x)+1)+' - ій черзі: '+ x for x in light_status_groups))
    
    return await bot.send_message(message.from_user.id, text_message, reply_markup=markup)



async def show_schedule(bot, query):
    groups = getCitiesGroups(query)
    
    city_name = query.message.text.split("м.")
    city_name = city_name[1].split(":")
    city_name = city_name[0]
    
    text_schedule = ""
    
    for group in groups:
        
        for schedule in group['schedule']:
            if schedule['light'] == 'on':
               text_schedule += str(schedule['time'])+ " "
            else:
                text_schedule += "="
            if group['schedule'].index(schedule) == len(group['schedule']) - 1 and not groups.index(group) == len(groups) - 1:
                text_schedule += "\n" 
             
             
    text_schedule = text_schedule.split("\n")
    text = ""
    
    for period_of_time in text_schedule:
        text += "⚡️ Черга №" + str(text_schedule.index(period_of_time)+1) + ":\n" 
        period_of_time = period_of_time.split("=")
        for x in period_of_time:
            if not x == '':
                mass = [int(i) for i in x.split()]
                mass.append(mass[len(mass)-1]+1)
                text += "⏱ " + str(mass[0]) + " - " + str(mass[len(mass)-1]) + "\n"
                
                
    print(text)
        
    
    text_message = ('<b>Погодинний розклад подачі електроенергії для м.'+city_name+'🇺🇦:</b>\n' + text)
    
    await bot.send_message(query.from_user.id, text_message, parse_mode='HTML')