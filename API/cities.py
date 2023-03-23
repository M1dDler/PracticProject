from flask import request, Response, Blueprint
from bson.json_util import dumps
from dotenv import load_dotenv
import os
import json
from API.dbConnect import settlements
from Parser.chernivtsi_parser import ChernivtsiParser
from Parser.ternopil_parser import TernopilParser

load_dotenv()

city = Blueprint('city', __name__)
parse_chernivtsi_url = os.getenv("CHERNIVTSI_PARSER_URL")
parse_ternopil_url = os.getenv("TERNOPIL_PARSER_URL")
apikey = os.getenv("APIKEY")

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
    try:
        city = dumps(settlements.find_one({"city_id" : city_id}))
        parsed_data = json.loads(city)
        groups = parsed_data['groups']

        for group in groups:
            if group['group'] == group_number:
                return Response(json.dumps(group), status=200, mimetype='application/json')
        return Response(status=404)
    except:
        return Response(status=404)
    
#Add city to database
@city.route('/cities', methods=['POST'])
def post():
    
    if len(request.headers) == 4:
        return Response(status=403, mimetype='application/json')
    if not request.headers['Bearer'] == apikey:
        return Response(status=403, mimetype='application/json')
    
    groups_range = range(1, 19)
    chernivtsi = ChernivtsiParser(groups_range, parse_chernivtsi_url)
    chernivtsi_schedules = chernivtsi.get_schedules()
    settlements.find_one_and_delete({'city_id' : chernivtsi_schedules['city_id']})
    settlements.insert_one(chernivtsi_schedules)
    
    ternopil = TernopilParser(parse_ternopil_url)
    ternopil_schedules = ternopil.get_schedules()
    settlements.find_one_and_delete({'city_id' : ternopil_schedules['city_id']})
    settlements.insert_one(ternopil_schedules)
    
    return Response(status=200, mimetype='application/json')