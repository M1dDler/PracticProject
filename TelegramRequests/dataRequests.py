import requests
import os
import json

def getCities():
    base_url = os.getenv("APIURL")
    end_point = '/cities'
    url = base_url + end_point
    cities = requests.get(url=url).json()
    return cities

def getCityByTitle(message):
    base_url = os.getenv("APIURL")
    end_point = '/cities'
    url = base_url + end_point
    cities = requests.get(url=url).json()
    
    for city in cities:
        if city['city_name'].lower() == message.text.lower():
            return city
    return None

def getCitiesGroups(query):
    query_text = query.data.split('_')
    query_text = query_text[1]
    
    base_url = os.getenv("APIURL")
    end_point = '/cities/'+query_text+'/groups'
    url = base_url + end_point
    groups = requests.get(url=url).json()
    return groups

def postNotifications(telegram_id, city_id, city_group):
    base_url = os.getenv("APIURL")
    apikey = os.getenv("APIKEY")
    
    headers = headers = {
                "Authorization": f"API-KEY {apikey}",
                'Content-Type': "application/json",
            }
    
    end_point = '/notifications/'+telegram_id+'/'+city_id+'/'+city_group
    
    url = base_url + end_point
    response = requests.post(url=url, headers=headers)
    
    return response.status_code 

def deleteNotifications(telegram_id):
    base_url = os.getenv("APIURL")
    apikey = os.getenv("APIKEY")
    
    headers = headers = {
                "Authorization": f"API-KEY {apikey}",
                'Content-Type': "application/json",
            }
    
    end_point = '/notifications/'+telegram_id
    
    url = base_url + end_point
    response = requests.delete(url=url, headers=headers)
    
    return response.status_code 