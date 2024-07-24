#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
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


@app.route('/campers', methods=['GET', 'POST'])
def campers():
    if request.method == 'GET':
        campers = []
        for camper in Camper.query.all():
            camper_dict = {
                'id': camper.id,
                'name': camper.name,
                'age': camper.age
            }
            campers.append(camper_dict)


        return make_response(jsonify(campers), 200)
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_camper = Camper(
                name=data.get('name'),
                age=data.get('age')            
            )
            db.session.add(new_camper)
            db.session.commit()

            return make_response(new_camper.to_dict(), 201)
        except:
            return make_response(jsonify({'errors': ['validation errors']}), 400)


@app.route('/campers/<int:id>', methods=['GET', 'PATCH'])
def camper_by_id(id):
    camper = Camper.query.filter(Camper.id == id).first()

    if camper == None:
        return make_response(jsonify({'error': 'Camper not found'}), 404)

    else:
        if request.method == 'GET':
            return make_response(camper.to_dict(), 200)
        elif request.method == 'PATCH':
            try:
                data = request.get_json()
                for attr, value in data.items():
                    setattr(camper, attr, value)

                db.session.add(camper)
                db.session.commit()

                return make_response(camper.to_dict(), 202)
            except:
                return make_response(jsonify({'errors': ['validation errors']}), 400)

@app.route('/activities')
def activities():
    activities = []
    for activity in Activity.query.all():
        activity_dict = {
            'id': activity.id,
            'name': activity.name,
            'difficulty': activity.difficulty
        }
        activities.append(activity_dict)

    return make_response(jsonify(activities), 200)

@app.route('/activities/<int:id>', methods=['DELETE'])
def activity_by_id(id):
    activity = Activity.query.filter(Activity.id == id).first()

    if activity is None:
        return make_response(jsonify({'error': 'Activity not found'}), 404)
    
    elif request.method == 'DELETE':
        db.session.delete(activity)
        db.session.commit()

        return make_response({}, 204)
    
@app.route('/signups', methods=['POST'])
def signups():
    if request.method == 'POST':
        try:
            data = request.get_json()
            new_signup = Signup(
                time=data.get('time'),
                camper_id=data.get('camper_id'),
                activity_id=data.get('activity_id')            
            )
            db.session.add(new_signup)
            db.session.commit()

            return make_response(new_signup.to_dict(), 201)
        except:
            return make_response(jsonify({'errors': ['validation errors']}), 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)