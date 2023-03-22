import requests
import os
from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=100, ttl=3600))
def getCities():
    base_url = os.getenv("APIURL")
    end_point = '/cities'
    url = base_url + end_point
    cities = requests.get(url=url).json()
    return cities

@cached(cache=TTLCache(maxsize=100, ttl=3600))
def getCityById(city_id):
    base_url = os.getenv("APIURL")
    end_point = '/cities/'+city_id
    url = base_url + end_point
    city = requests.get(url=url).json()
    return city
    
def getNotifications(telegram_id, city_id):
    base_url = os.getenv("APIURL")
    apikey = os.getenv("APIKEY")
    
    headers = headers = {
                "Bearer": apikey,
                'Content-Type': "application/json",
            }
    
    end_point = '/notifications/'+telegram_id+"/"+city_id
    
    url = base_url + end_point
    notifications = requests.get(url=url, headers=headers).json()
    
    return notifications
    

def postNotifications(telegram_id, city_id, city_group):
    base_url = os.getenv("APIURL")
    apikey = os.getenv("APIKEY")
    
    headers = headers = {
                "Bearer": apikey,
                'Content-Type': "application/json",
            }
    
    end_point = '/notifications/'+telegram_id+'/'+city_id+'/'+city_group
    
    url = base_url + end_point
    response = requests.post(url=url, headers=headers)
    
    return response.status_code 

def deleteNotifications(telegram_id, city_id, city_group):
    base_url = os.getenv("APIURL")
    apikey = os.getenv("APIKEY")
    
    headers = headers = {
                "Bearer": apikey,
                'Content-Type': "application/json",
            }
    
    end_point = '/notifications/'+telegram_id+"/"+city_id+"/"+city_group
    
    url = base_url + end_point
    response = requests.delete(url=url, headers=headers)
    
    return response.status_code 