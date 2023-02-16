#!/urs/bin/python3
"""retrieve a data about the city"""

from flask import jsonify, make_response, request, abort
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views

@app_views.route('/cities', methods=['GET'])
def get_all_cities():
    """retrieve all cities"""
    cities = storage.all('City')
    return jsonify(cities.to_dict())

@app_views.route('/states/<state_id>/cities', methods=['GET'])
def retrieve_cities_states(state_id):
    """retrieve cities in specific state"""
    state = storage.get(state_id, state)
    if not state:
        abort(404)
    for city in state.cities:
        return make_response(jsonify(city.to_dict()))
@app_views.route('/cities/<city_id>')
def get_city_by_id(city_id):
    """get the cities by id"""
    city = storage.get(city_id, City)
    if not city:
        abort(404)
    return make_response(jsonify(city.to_dict()))

@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """deletes a city with an id """
    city = storage.get(city_id, City)
    if not city:
        abort(404)
    city.delete()
    city.save()
    return jsonify({}, 200)

@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_new(state_id):
    """create a new city in specific state"""
    state = storage.get(state_id, State)
    if not state:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error":"Not a JSON"}), 400)
    if not "name" in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_object = City(**request.get_json())
    new_object.save()
    return jsonify(new_object.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    """update a specific city"""
    city = storage.get(city_id, City)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 404)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)