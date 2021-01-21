"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from sms import send
from datastructures import Queue
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
queue=Queue()
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    
    response_body = {
        "msg": "Client Added ",
        "resp": queue.get_queue()
    }

    return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def handle_enqueue():
    newClient = request.get_json()
    queue.enqueue(newClient)
    if newClient is None:
            return "The enqueue request body is null", 400
    response_body = {
        "enqueued": newClient,
        "resp": queue.get_queue()
    }
    return jsonify(response_body), 200

@app.route('/userdequeue', methods=['DELETE'])
def handle_dequeue():
    
    user=queue.dequeue()
    send(body='',to=user['phone'] )
    if user is None:
        return "The dequeue request body is null", 400
    response_body = {
        "dequeued": user,
        "resp": queue.get_queue()
    }
    return jsonify(response_body),200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
