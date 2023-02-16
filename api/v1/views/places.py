#!/usr/bin/python3
"""places objects that handles all the api"""

from flask import make_response, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=['GET'])
def get_places(city_id):
    """get places of a specific city"""
    city = storage.get(city_id, City)
    if not city:
        abort(404)
    for place in city.places:
        return jsonify(place.to_dict()), 200
    
@app_views.route("/places/<place_id>", methods=["GET"])
def get_specific_place(place_id):
    """get specific place using the id"""
    place = storage.get(place_id, Place)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """deleting a place from the data"""
    place = storage.get(place_id, Place)
    if not place:
        abort(404)
    place.delete()
    place.save()
    return jsonify({}), 200

@app_views.route("/cities/<city_id>/places")
def create_place(city_id):
    """create a new place"""
    city = storage.get(city_id, City)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 404)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 404)
    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 404)
    if not storage.get(request.get_json()['user_id'], 'User'):
        abort(404)
    new_place = Place(**request.get_json())
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict())

@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """update a specific place"""
    place = storage.get(place_id, Place)
    if not request.get_json():
        return make_response(jsonify({"error":"Not a JSON"}))
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k , v)
    place.save()
    return jsonify(place.to_dict())
