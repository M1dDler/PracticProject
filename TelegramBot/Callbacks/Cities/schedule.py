from TelegramBot.DataBase.dbRequests import getCityById

async def show_schedule(bot, query):
    power_grid = ['on', 'maybe', 'off']
    
    for power_grid_status in power_grid:
    
        city_id = query.data.split('_')
        city_id = city_id[1]
        
        city = getCityById(city_id)
        groups = city['groups']
        
        city_name = query.message.text.split("м.")
        city_name = city_name[1].split(":")
        city_name = city_name[0]
        
        text_schedule = ""
        
        for group in groups:
            
            for schedule in group['schedule']:
                if schedule['light'] == power_grid_status:
                    text_schedule += str(schedule['time'])+ " "
                else:
                    text_schedule += "="
                if group['schedule'].index(schedule) == len(group['schedule']) - 1 and not groups.index(group) == len(groups) - 1:
                    text_schedule += "\n" 
                
                
        text_schedule = text_schedule.split("\n")
        text = ""
        
        is_schedule = False
        for period_of_time in range (len(text_schedule)):
            text += "⚡️ Черга №" + str(period_of_time+1) + ":\n" 
            text_schedule[period_of_time] = text_schedule[period_of_time].split("=")
            for x in text_schedule[period_of_time]:
                if not x == '':
                    mass = [int(i) for i in x.split()]
                    mass.append(mass[len(mass)-1]+1)
                    is_schedule = True
                    text += "⏱ " + str(mass[0]) + " - " + str(mass[len(mass)-1]) + "\n"
        
        if is_schedule:
            if power_grid_status == 'on':
                text_message = ('<b>✅ Погодинний розклад подачі електроенергії для м.'+city_name+'🇺🇦:</b>\n' + text)
                await bot.send_message(query.from_user.id, text_message, parse_mode='HTML', timeout=30)
            if power_grid_status == 'maybe':
                text_message = ('<b>⚠️ Погодинний розклад можливого включення/виключення електроенергії для м.'+city_name+'🇺🇦:</b>\n' + text)
                await bot.send_message(query.from_user.id, text_message, parse_mode='HTML', timeout=30)
            if power_grid_status == 'off':
                text_message = ('<b>❌ Погодинний розклад виключення електроенергії для м.'+city_name+'🇺🇦:</b>\n' + text)
                await bot.send_message(query.from_user.id, text_message, parse_mode='HTML', timeout=30)