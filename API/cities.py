from flask import request, Response, Blueprint
from bson.json_util import dumps
import json
from API.dbConnect import settlements
from Parser.chernivtsi_parser import ChernivtsiParser
from API.authorization import authorization

city = Blueprint('city', __name__)

#Get all cities
@city.route('/cities')
def get_cities():
    cities = dumps(list(settlements.find()))
    if cities == 'null':
        return Response(status=404)
    return Response(cities, status=200, mimetype='application/json')  

#Get city
@city.route('/cities/<city_id>')
def get_city_id(city_id):
    city = dumps(settlements.find_one({"city_id" : city_id}))
    if city == 'null':
        return Response(status=404)
    return Response(city, status=200, mimetype='application/json')

#Get groups from city
@city.route('/cities/<city_id>/groups')
def get_cities_groups(city_id):
    try:
        city = dumps(settlements.find_one({"city_id" : city_id}))
        parsed_data = json.loads(city)
        groups = parsed_data['groups']
        return Response(json.dumps(groups), status=200, mimetype='application/json')
    except:
        return Response(status=404)

#Get group from city
@city.route('/cities/<city_id>/groups/<group_number>')
def get_cities_group(city_id, group_number):
    city = dumps(settlements.find_one({"city_id" : city_id}))
    parsed_data = json.loads(city)
    groups = parsed_data['groups']

    for group in groups:
        if group['group'] == group_number:
            return Response(json.dumps(group), status=200, mimetype='application/json')
    return Response(status=404)

#Add city to database
@city.route('/cities', methods=['POST'])
def post():
    
    if not authorization(request.headers['Authorization']):
        return Response(status=403, mimetype='application/json')
    
    parse_url = 'https://oblenergo.cv.ua/shutdowns/?next'
    groups_range = range(1, 19)
    p = ChernivtsiParser(groups_range, parse_url)
    schedules = p.get_schedules()
    settlements.find_one_and_delete({'city_id' : schedules['city_id']})
    settlements.insert_one(schedules)
    return Response(status=200, mimetype='application/json')