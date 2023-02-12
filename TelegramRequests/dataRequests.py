import requests
import os
import json

def getCities():
    base_url = os.getenv("DATABASEURL")
    end_point = '/cities'
    url = base_url + end_point
    cities = requests.get(url=url).json()
    return cities

def getCityByTitle(message):
    base_url = os.getenv("DATABASEURL")
    end_point = '/cities'
    url = base_url + end_point
    cities = requests.get(url=url).json()
    
    for city in cities:
        if city['city_name'] == message.text:
            return city
    return None