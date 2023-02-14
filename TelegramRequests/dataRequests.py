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


def getCitiesGroups(query):
    query_text = query.data.split('_')
    query_text = query_text[1]
    
    base_url = os.getenv("DATABASEURL")
    end_point = '/cities/'+query_text+'/groups'
    url = base_url + end_point
    groups = requests.get(url=url).json()
    return groups