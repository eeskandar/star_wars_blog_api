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
    
@app.route('/user/favorites', methods=['GET']) #da para solo un user al no ser dinámico
def get_user_favs():
    get_favs = Favorites.query.filter_by(user_id = "1")
    favs_list = list(map(lambda fav: fav.serialize(), get_favs))
  
    return jsonify(favs_list), 200

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
def get_person(people_id):
    get_person = Characters.query.get_or_404(people_id)

    response_body = {
        "character": get_person.character_name,
        "birth_year": get_person.birth_year,
        "gender": get_person.gender,
        "skin_color": get_person.skin_color,
        "heigth": get_person.heigth
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    get_planet = Planets.query.get_or_404(planet_id)

    response_body = {
        "planet_name": get_planet.planet_name,
        "climate": get_planet.climate,
        "terrain": get_planet.terrain,
        "population": get_planet.population
    }
    return jsonify(response_body), 200


# the POST methods
@app.route('/user', methods=['POST'])
def post_user():
    body = request.json    #sacando la info necesaria a un diccionario
    new_user = User.create(body)    #pasando la información dentro de nuestra clase y vertiendo la info contenida en body

    if type(new_user) == dict:    #en caso de haber un error se devuelve esto
        return jsonify({
            "msg": new_user["msg"]
        }), new_user["status"]

    response_body = {      #en caso de salir todo bien se devuelve esto
        "user": new_user.serialize()
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['POST'])
def post_people():
    body = request.json   
    new_char = Characters.create(body)
    if type(new_char) == dict:
        return jsonify({
            "msg": new_char["msg"]
        }), new_char["status"]

    response_body = {
        "character": new_char.serialize()
    }
    return jsonify(response_body), 200
    
@app.route('/planets', methods=['POST'])
def post_planets():
    body = request.json 
    new_planet = Planets.create(body) 
    if type(new_planet) == dict:
        return jsonify({
            "msg": new_planet["msg"]
        }), new_planet["status"]

    response_body = {
        "planet": new_planet.serialize()
    }
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_fav_person(people_id):
    body = request.json
    new_fav_char = Favorites.fav_char(Favorites, body, people_id)

    if type(new_fav_char) == dict:
        return jsonify({
            "msg": new_fav_char["msg"]
        }), new_fav_char["status"]

    response_body = {
        "favorite": new_fav_char.serialize_char()
    }

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_fav_planet(planet_id):
    body = request.json
    new_fav_planet = Favorites.fav_planet(Favorites, body, planet_id)

    if type(new_fav_planet) == dict:
        return jsonify({
            "msg": new_fav_planet["msg"]
        }), new_fav_planet["status"]

    response_body = {
        "favorite": new_fav_planet.serialize_planet()
    }

    return jsonify(response_body), 200


# the DELETE methods
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_person(people_id):
    get_characters = Favorites.query.filter_by(character_id = people_id).first() # works when deleting from id, not from character_id
    print(get_characters)
    delete_instance = Favorites.delete_and_commit(get_characters)

    if delete_instance is False:
        return jsonify ({
            "msg": "Could not delete your favs"
        }), 400

    response_body = {
        "msg": "Favorites deleted successfully"
    }
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    get_planets = Favorites.query.filter_by(planet_id = planet_id).first()
    delete_instance = Favorites.delete_and_commit(get_planets)

    if delete_instance is False:
        return jsonify ({
            "msg": "Could not delete your favs"
        }), 400

    response_body = {
        "msg": "Favorites deleted successfully"
    }
    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
