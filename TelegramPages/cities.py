import datetime
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from TelegramRequests.dataRequests import *
import pytz

async def cities(bot, message):
    cities = getCities()
    
    if len(cities) == 0:
        return await bot.send_message(message.from_user.id, "В списку немає жодного населеного пункту! 😣")
    
    text_message = "<b>Інформація про подачу електроенергії доступна для таких міст:</b> ⤵️\n\n" + "\n".join(str('📌 '+x['city_name']) for x in cities)
    await bot.send_message(chat_id=message.from_user.id, text=text_message +'\n\n'+
                           'Для відображення детальної інформації введіть в чат назву населеного пункту ✏️'
                           ,parse_mode='HTML')
    
    
async def findCityByTitle(bot, message):
    city = getCityByTitle(message)
    
    if city == None:
        return await bot.send_message (message.from_user.id, 'Вказаного вами населеного пункту, не знайдено! 🙄\n'
                                       + 'Для перегляду списку всіх населених пунктів скористайтесь контекстним меню ⬇️')
    
    now_utc = datetime.datetime.now(pytz.UTC)
    
    gmt2 = pytz.timezone('Etc/GMT-2')
    now_gmt2 = now_utc.astimezone(gmt2)
    current_time = now_gmt2.strftime('%H:%M:%S')
    
    time_to_find = current_time.split(":")
    
    if time_to_find[0][0] == "0":
        time_to_find[0] = time_to_find[0][1]
    
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
                    "❕ Станом на "+current_time+", статус електромережі в \n"+"\n".join('=== '+str(light_status_groups.index(x)+1)+' - ій черзі: '+ x for x in light_status_groups))
    
    return await bot.send_message(message.from_user.id, text_message, reply_markup=markup)



async def show_schedule_on(bot, query):
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
    
    
    text_message = ('<b>✅ Погодинний розклад подачі електроенергії для м.'+city_name+'🇺🇦:</b>\n' + text)
    
    await bot.send_message(query.from_user.id, text_message, parse_mode='HTML')
    
    
    
async def show_schedule_maybe(bot, query):
    groups = getCitiesGroups(query)
    
    city_name = query.message.text.split("м.")
    city_name = city_name[1].split(":")
    city_name = city_name[0]
    
    text_schedule = ""
    
    for group in groups:
        
        for schedule in group['schedule']:
            if schedule['light'] == 'maybe':
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
                
    
    text_message = ('<b>⚠️ Погодинний розклад можливого включення/виключення електроенергії для м.'+city_name+'🇺🇦:</b>\n' + text)
    
    await bot.send_message(query.from_user.id, text_message, parse_mode='HTML')
    
    
    
async def show_schedule_off(bot, query):
    groups = getCitiesGroups(query)
    
    city_name = query.message.text.split("м.")
    city_name = city_name[1].split(":")
    city_name = city_name[0]
    
    text_schedule = ""
    
    for group in groups:
        
        for schedule in group['schedule']:
            if schedule['light'] == 'off':
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
        
    
    text_message = ('<b>❌ Погодинний розклад виключення електроенергії для м.'+city_name+'🇺🇦:</b>\n' + text)
    
    await bot.send_message(query.from_user.id, text_message, parse_mode='HTML')
    

async def notification(bot, query):
    groups = getCitiesGroups(query)
    city_id  = query.data.split("_") 
    city_id = city_id[1]
    
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
    delete_btn = types.InlineKeyboardButton("Вимкнути наявні сповіщення 🔇", callback_data="delete_group_"+str(query.from_user.id))
    list_buttons = [one_btn, two_btn, three_btn, four_btn, five_btn, six_btn, seven_btn, eight_btn, nine_btn, ten_btn]
    row_buttons = []
    for x in groups:
        row_buttons.append(list_buttons[groups.index(x)])
        
    markup.row(*row_buttons)
    markup.add(delete_btn)
    return await bot.send_message(query.from_user.id, "Оберіть номер черги для отримання сповіщення 🔖", reply_markup=markup)
    