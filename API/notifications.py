from flask import request, Response, Blueprint
from API.dbConnect import notifications
import datetime
import requests
import os
from dotenv import load_dotenv
import pytz
from bson.json_util import dumps

load_dotenv()

notification = Blueprint('notification', __name__)
apikey = os.getenv("APIKEY")

#Add user notification
@notification.route('/notifications/<int:telegram_id>/<city_id>/<int:city_group>', methods=['POST'])
def post_notification(telegram_id, city_id, city_group):
    
    try:
        if not request.headers['Bearer'] == apikey:
            return Response(status=403, mimetype='application/json')
    except:
        return Response(status=403, mimetype='application/json')
    
    data = {
             "telegram_id": telegram_id,
             "city_id": city_id,
             "city_group": city_group
           }
    
    findData = notifications.find_one(data)
    
    if findData == None:
        notifications.insert_one(data)
        return Response(status=200, mimetype='application/json')
    return Response(status=406, mimetype='application/json')

#Telegram send notifications
@notification.route('/notifications', methods=['POST'])
def post_notifications():
    
    try:
        if not request.headers['Bearer'] == apikey:
            return Response(status=403, mimetype='application/json')
    except:
        return Response(status=403, mimetype='application/json')
        
    
    token = os.getenv("BOTTOKEN")
    url = 'https://api.telegram.org/bot'+token+'/sendMessage'
    databaseUrl = os.getenv("APIURL")
    
    result = list(notifications.find())
    cities = requests.get(url=databaseUrl+'/cities').json()
    
    now_utc = datetime.datetime.now(pytz.UTC)
    
    gmt2 = pytz.timezone('Etc/GMT-2')
    now_gmt2 = now_utc.astimezone(gmt2)
    current_time = now_gmt2.strftime('%H')
    
    if current_time[0] == "0":
        current_time = current_time.replace(current_time, current_time[1])

    current_time = int(current_time)
    

    messages = {
        'on': {
            'off': "❌ Увага, через годину в м.{city_name}, в {group_number}-ій черзі передбачається відключення електроенергії😢",
            'maybe': "⚠️❌ Увага, через годину в м.{city_name}, в {group_number}-ій черзі передбачається можливе виключення електроенергії 😏",
        },
        'off': {
            'on': "✅ Увага, через годину в м.{city_name}, в {group_number}-ій черзі передбачається включення електроенергії 😊",
            'maybe': "⚠️✅ Увага, через годину в м.{city_name}, в {group_number}-ій черзі передбачається можливе включення електроенергії 😇",
        },
        'maybe': {
            'on': "✅ Увага, через годину в м.{city_name}, в {group_number}-ій черзі передбачається 100%-ва подача електроенергії 😁",
            'off': "❌ Увага, через годину в м.{city_name}, в {group_number}-ій черзі передбачається відключення електроенергії😢",
        },
    }
    
    for x in result:
        try:
            text = " "
            
            filter_city = [city for city in cities if city["city_id"] == x["city_id"]]
            if len(filter_city) == 0:
                continue
            filter_group = [group for group in filter_city[0]["groups"] if str(group["group"]) == str(x["city_group"])]
            if len(filter_group) == 0:
                continue
            filter_schedule_current = [schedule for schedule in filter_group[0]["schedule"] if schedule["time"] == current_time]
            if len(filter_schedule_current) == 0:
                continue 
            
            
            if not current_time == 23: 
                filter_schedule = [schedule for schedule in filter_group[0]["schedule"] if schedule["time"] == current_time + 1]
            else:
                filter_schedule = [schedule for schedule in filter_group[0]["schedule"] if schedule["time"] == 0]
            
            current_schedule = filter_schedule_current[0]["light"]
            future_schedule = filter_schedule[0]["light"]
            city_name = filter_city[0]["city_name"]
            group_number = str(filter_group[0]["group"])

            text = messages[current_schedule][future_schedule].format(
                city_name=city_name,
                group_number=group_number,
            )

            data = {
                    "chat_id": x["telegram_id"],
                    "text": text
                }
            
            requests.post(url=url, data=data)
            
        except:
            continue

    return Response(status=200, mimetype='application/json')

#get user notifications from city
@notification.route('/notifications/<int:telegram_id>/<city_id>')
def get_user_notifications(telegram_id, city_id): 
    
    try:
        if not request.headers['Bearer'] == apikey:
            return Response(status=403, mimetype='application/json')
    except:
        return Response(status=403, mimetype='application/json')
    
    result = dumps(notifications.find({"telegram_id": telegram_id,
                                       "city_id": city_id }))

    return Response(result, status=200, mimetype='application/json')

#delete user notification
@notification.route('/notifications/<int:telegram_id>/<city_id>/<int:city_group>', methods=['DELETE'])
def delete_notifications(telegram_id, city_id, city_group):
    
    try:
        if not request.headers['Bearer'] == apikey:
            return Response(status=403, mimetype='application/json')
    except:
        return Response(status=403, mimetype='application/json')
        
    deletedata = dumps(notifications.find({"telegram_id": telegram_id,
                                          "city_id": city_id,
                                          "city_group": city_group}))
    
    if deletedata == "[]":
        return Response(status=404, mimetype='application/json')
    notifications.delete_many({"telegram_id": telegram_id,
                                "city_id": city_id,
                                "city_group": city_group})
    
    return Response(status=200, mimetype='application/json')