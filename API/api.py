from pymongo import MongoClient
from flask import Flask, request, Response
from bson.json_util import dumps
from threading import Thread
import json

global client

client = MongoClient('localhost', 27017)
client.server_info()
db = client["Dtek"]
collection = db["settlements"]

app = Flask("") 
@app.route("/")
def hello():
    return "Hello, World!"
 
@app.route('/post', methods=['POST'])
def post():
    data = request.json
    result = collection.insert_one(data)
    return Response(status=200, mimetype='application/json')

@app.route('/cities')
def get_cities():
    cities = dumps(list(collection.find()))
    if cities == 'null':
        return Response(status=404)
    return Response(cities, status=200, mimetype='application/json')  

@app.route('/cities/<city_id>')
def get_city_id(city_id):
    city = dumps(collection.find_one({"city_id" : city_id}))
    if city == 'null':
        return Response(status=404)
    return Response(city, status=200, mimetype='application/json')

@app.route('/cities/<city_id>/groups')
def get_cities_groups(city_id):
    try:
        city = dumps(collection.find_one({"city_id" : city_id}))
        parsed_data = json.loads(city)
        groups = parsed_data['groups']
        return Response(json.dumps(groups), status=200, mimetype='application/json')
    except:
        return Response(status=404)

@app.route('/cities/<city_id>/groups/<int:group_number>')
def get_cities_group(city_id, group_number):
    city = dumps(collection.find_one({"city_id" : city_id}))
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