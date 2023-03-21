from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

apikey = os.getenv("APIKEY")
dataBaseUrl = os.getenv("DATABASEURL")
client = MongoClient(dataBaseUrl)
client.server_info()

db = client["Dtek"]
settlements = db["settlements"]
notifications = db["notifications"]
