from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    favorites = db.relationship("Favorites", backref="favorites_user")

    @classmethod
    def create(cls, body):
        try:
            if body.get("first_name") is None:
                raise Exception ({
                    "msg": "Your first name can't be empty"
                })
            if body.get("last_name") is None:
                raise Exception ({
                    "msg": "Your last name can't be empty"
                })
            if body.get("password") is None:
                raise Exception ({
                    "msg": "Your password can't be empty"
                })
            if body.get("email") is None:
                raise Exception ({
                    "msg": "Your email can't be empty"
                })

            user_exist = cls.query.filter_by(email = body["email"]).one_or_none()

            if user_exist:
                raise Exception ({
                    "msg": "This email is already registered. Try another one"
                })
            
            new_user = cls(first_name = body["first_name"], last_name = body["last_name"], email = body["email"], password = body["password"])

            if not isinstance(new_user, cls):
                raise Exception ({
                    "msg": "There's no response from the server"
                })
            
            save_instance = new_user.save_and_commit()

            return new_user
            
        except Exception as error:
            print(error.args)
            return ({
                "msg": "Something went wrong (" + error.args[0]["msg"] + ")"
            })

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "name": self.first_name + " " + self.last_name,
            "email": self.email
        }

    def save_and_commit(self):
        try:
            db.session.add(self) 
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(50), unique=True, nullable=False)
    birth_year = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    heigth = db.Column(db.String(50))
    favorites = db.relationship("Favorites", backref="favorites_char")

    @classmethod
    def create(cls, body):
        try:
            if body.get("character_name") is None:
                raise Exception ({
                    "msg": "Your must write the character's name"
                })

            character_exist = cls.query.filter_by(character_name = body["character_name"]).one_or_none()

            if character_exist:
                raise Exception ({
                    "msg": "This character is already registered. Try another one or adding more info to the name"
                })
            
            new_character = cls(character_name = body["character_name"], birth_year = body["birth_year"], gender = body["gender"], skin_color = body["skin_color"], heigth = body["heigth"])

            if not isinstance(new_character, cls):
                raise Exception ({
                    "msg": "There's no response from the server"
                })
            
            save_instance = new_character.save_and_commit()

            return new_character
            
        except Exception as error:
            print(error.args)
            return ({
                "msg": "Something went wrong (" + error.args[0]["msg"] + ")"
            })

    def __repr__(self):
        return f'<Character {self.character_name}>'

    def serialize(self):
        return {
            "name": self.character_name
        }

    def save_and_commit(self):
        try:
            db.session.add(self) 
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(50), unique=True, nullable=False)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    population = db.Column(db.String(50))
    favorites = db.relationship("Favorites", backref="favorites_planet")

    @classmethod
    def create(cls, body):
        try:
            if body.get("planet_name") is None:
                raise Exception ({
                    "msg": "Your must write the planet's name"
                })

            planet_exist = cls.query.filter_by(planet_name = body["planet_name"]).one_or_none()

            if planet_exist:
                raise Exception ({
                    "msg": "This planet is already registered. Try another one or adding more info to the name"
                })
            
            new_planet = cls(planet_name = body["planet_name"], climate = body["climate"], terrain = body["terrain"], population = body["population"])

            if not isinstance(new_planet, cls):
                raise Exception ({
                    "msg": "There's no response from the server"
                })
            
            save_instance = new_planet.save_and_commit()

            return new_planet
            
        except Exception as error:
            print(error.args)
            return ({
                "msg": "Something went wrong (" + error.args[0]["msg"] + ")"
            })

    def __repr__(self):
        return f'<Planet {self.planet_name}>'

    def serialize(self):
        return {
            "name": self.planet_name
        }

    def save_and_commit(self):
        try:
            db.session.add(self) 
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)

    def __repr__(self):
        return f'<Favorites {self.id}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "fav_char": self.character_id,
            "fav_planet": self.planet_id
        }
    
    def save_and_commit(self):
        try:
            db.session.add(self) 
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return False