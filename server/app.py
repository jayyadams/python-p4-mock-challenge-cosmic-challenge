#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/planets', methods = ['GET'])
def planets():
    planets = Planet.query.all()
    planets_dict = [planet.to_dict() for planet in planets]
    response = make_response(
        planets_dict, 200
    )
    return response

@app.oroute('/missions', methods = ['POST'])
def missions():
    form_data = request.get_json()
    try:
        new_mission = Mission(
            name = form_data['name'],
            scientist_id = form_data['scientist_id'],
            planet_id = form_data['[planet_id]']
        )
        db.session.add(new_mission)
        db.session.commit()
        response = make_response(
            new_mission.to_dict(), 200
        )
    except ValueError:
        response = make_response(
            {"errors": ["validation errors"]}, 400
        )
    return response 


if __name__ == '__main__':
    app.run(port=5555, debug=True)
