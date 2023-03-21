import os
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv("APIKEY")

#API key validation
def authorization(auth):
    auth = auth.split(" ")
    if not len(auth) == 2:
        return False
    
    if auth[1] == apikey:
        return True
    return False

