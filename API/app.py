from flask import Flask, Response
from threading import Thread
from waitress import serve
from API.cities import city
from API.notifications import notification

app = Flask(__name__)
app.register_blueprint(city)
app.register_blueprint(notification)

@app.route('/')
def hello():
    return Response(status=200, mimetype='application/json')
    
def run():
    serve(app, host="0.0.0.0", port=80)
 
def keep_alive():
    t = Thread(target=run)
    t.start()