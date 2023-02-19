from pymongo import MongoClient
from flask import Flask, request, Response
from bson.json_util import dumps
from threading import Thread
from dotenv import load_dotenv
import datetime
import json
import os
import requests
import asyncio

load_dotenv()

global client

dataBaseUrl = os.getenv("DATABASEURL")
client = MongoClient(dataBaseUrl)
client.server_info()
db = client["Dtek"]
settlements = db["settlements"]
notifications = db["notifications"]

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/notifications/<int:telegram_id>/<city_id>/<int:city_group>', methods=['POST'])
def post_notifications(telegram_id, city_id, city_group):
    
    data = {
             "telegram_id": telegram_id,
             "city_id": city_id,
             "city_group": city_group
           }
    
    result = notifications.insert_one(data)
    return Response(status=200, mimetype='application/json')

@app.route('/notifications', methods=['POST'])
def get_notifications():
    apikey = os.getenv("APIKEY")
    
    try:
        token = request.headers['Authorization'].split(" ")
        if not token[1] == apikey:
            return Response(status=403, mimetype='application/json')
    except:
        return Response(status=403, mimetype='application/json')
        
    
    token = os.getenv("BOTTOKEN")
    url = 'https://api.telegram.org/bot'+token+'/sendMessage'
    databaseUrl = os.getenv("APIURL")
    
    result = list(notifications.find())
    cities = requests.get(url=databaseUrl+'/cities').json()
    current_time = str(datetime.datetime.now().time())
    current_time = current_time.split(":")
    current_time = int(current_time[0])
    if current_time == 00:
        current_time = 0
    
    for x in result:
        
        text = " "
        
        filter_city = [city for city in cities if city["city_id"] == x["city_id"]]
        if len(filter_city) == 0:
            continue
        filter_group = [group for group in filter_city[0]["groups"] if group["group"] == x["city_group"]]
        if len(filter_group) == 0:
            continue
        filter_schedule_current = [schedule for schedule in filter_group[0]["schedule"] if schedule["time"] == current_time]
        if len(filter_schedule_current) == 0:
            continue 
        filter_schedule = [schedule for schedule in filter_group[0]["schedule"] if schedule["time"] == current_time + 1]
        
        if filter_schedule_current[0]["light"] == "on" and filter_schedule[0]["light"] == "off":
             text = ("❌ Увага, через годину в м."+filter_city[0]["city_name"]+", в "+str(filter_group[0]["group"])+"-ій черзі передбачається відключення електроенергії😢")
        
        elif filter_schedule_current[0]["light"] == "off" and filter_schedule[0]["light"] == "on":
             text = ("✅ Увага, через годину в м."+filter_city[0]["city_name"]+", в "+str(filter_group[0]["group"])+"-ій черзі передбачається включення електроенергії 😊")

        elif filter_schedule_current[0]["light"] == "maybe" and filter_schedule[0]["light"] == "on":
             text = ("✅ Увага, через годину в м."+filter_city[0]["city_name"]+", в "+str(filter_group[0]["group"])+"-ій черзі передбачається 100%-ва подача електроенергії 😁")
        
        elif filter_schedule_current[0]["light"] == "on" and filter_schedule[0]["light"] == "maybe":
             text = "⚠️❌ Увага, через годину в м."+filter_city[0]["city_name"]+", в "+str(filter_group[0]["group"])+"-ій черзі передбачається можливе виключення електроенергії 😏"
             
        elif filter_schedule_current[0]["light"] == "off" and filter_schedule[0]["light"] == "maybe":
             text = "⚠️✅ Увага, через годину в м."+filter_city[0]["city_name"]+", в "+str(filter_group[0]["group"])+"-ій черзі передбачається можливе включення електроенергії 😇"
        
        elif filter_schedule_current[0]["light"] == "maybe" and filter_schedule[0]["light"] == "off":
             text = ("❌ Увага, через годину в м."+filter_city[0]["city_name"]+", в "+str(filter_group[0]["group"])+"-ій черзі передбачається відключення електроенергії😢")
             
        data = {
                 "chat_id": x["telegram_id"],
                 "text": text
               }
        
        requests.post(url=url, data=data)
    
    return Response(dumps(result), status=200, mimetype='application/json')


@app.route('/notifications/<int:telegram_id>', methods=['DELETE'])
def delete_notifications(telegram_id):
    notifications.delete_many({"telegram_id": telegram_id})
    return Response(status=200, mimetype='application/json')

@app.route('/post', methods=['POST'])
def post():
    data = request.json
    result = settlements.insert_one(data)
    return Response(status=200, mimetype='application/json')

@app.route('/cities')
def get_cities():
    cities = dumps(list(settlements.find()))
    if cities == 'null':
        return Response(status=404)
    return Response(cities, status=200, mimetype='application/json')  

@app.route('/cities/<city_id>')
def get_city_id(city_id):
    city = dumps(settlements.find_one({"city_id" : city_id}))
    if city == 'null':
        return Response(status=404)
    return Response(city, status=200, mimetype='application/json')

@app.route('/cities/<city_id>/groups')
def get_cities_groups(city_id):
    try:
        city = dumps(settlements.find_one({"city_id" : city_id}))
        parsed_data = json.loads(city)
        groups = parsed_data['groups']
        return Response(json.dumps(groups), status=200, mimetype='application/json')
    except:
        return Response(status=404)

@app.route('/cities/<city_id>/groups/<int:group_number>')
def get_cities_group(city_id, group_number):
    city = dumps(settlements.find_one({"city_id" : city_id}))
    parsed_data = json.loads(city)
    groups = parsed_data['groups']

    for group in groups:
        if group['group'] == group_number:
            return Response(json.dumps(group), status=200, mimetype='application/json')
    return Response(status=404)
     
def run():
    app.run(host='0.0.0.0', port=80)
 
def keep_alive():
    t = Thread(target=run)
    t.start()