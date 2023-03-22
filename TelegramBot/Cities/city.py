from TelegramBot.dbRequests import getCities
import pytz
import datetime
from telebot import types

async def getCityByTitle(bot, message):
    cities = getCities()
    city = None
    
    for x in cities:
        if x['city_name'].lower() == message.text.lower():
            city = x
            break
    
    if city == None:
        return await bot.send_message (message.from_user.id, 'Вказаного вами населеного пункту, не знайдено! 🙄\n'
                                       + 'Для перегляду списку всіх населених пунктів скористайтесь контекстним меню ⬇️', timeout=30)
    
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
                    "❕ Станом на "+current_time+", статус електромережі в \n"+"\n".join('=== '+str(x+1)+' - ій черзі: '+ str(light_status_groups[x]) for x in range(len(light_status_groups))))
    
    return await bot.send_message(message.from_user.id, text_message, reply_markup=markup, timeout=30)