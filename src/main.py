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
from models import db, User, Characters, Planets, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# the GET methods
@app.route('/user', methods=['GET'])
def get_user():
    get_user = User.query.all()
    user_list = list(map(lambda user: user.serialize(), get_user))

    return jsonify(user_list), 200
    
@app.route('/user/favorites', methods=['GET']) #query for all the Favorites instances where the user_id appears
def get_user_favs():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    get_characters = Characters.query.all()
    characters_list = list(map(lambda char: char.serialize(), get_characters))

    return jsonify(characters_list), 200
    
@app.route('/planets', methods=['GET'])
def get_planets():
    get_planets = Planets.query.all()
    planets_list = list(map(lambda planet: planet.serialize(), get_planets))

    return jsonify(planets_list), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


# the POST methods
@app.route('/user', methods=['POST'])
def post_user():
    body = request.json    #sacando la info necesaria a un diccionario
    new_user = User.create(body) #pasando la información dentro de nuestra clase y vertiendo la info contenida en body

    if type(new_user) == dict:
        return jsonify(new_user), 400

    response_body = {
        "user": new_user.serialize()
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['POST'])
def post_people():
    body = request.json   
    new_char = Characters.create(body)
    if type(new_char) == dict:
        return jsonify(new_char), 400

    response_body = {
        "character": new_char.serialize()
    }
    return jsonify(response_body), 200
    
@app.route('/planets', methods=['POST'])
def post_planets():
    body = request.json 
    new_planet = Planets.create(body) 
    if type(new_planet) == dict:
        return jsonify(new_planet), 400

    response_body = {
        "planet": new_planet.serialize()
    }
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_fav_person():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_fav_planet():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200


# the DELETE methods
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_person():
    response_body = {
        "msg": "Hello, this is your GET /user response"
    }
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet():
    response_body = {
        "msg": "Hello, this is your GET /user response"
    }
    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
