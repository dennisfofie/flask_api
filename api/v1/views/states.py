#!/usr/bin/python3
"""return the states of the objects"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort , request
from models import storage
from models.state import State

@app_views.route("/states", methods=["GET"])
def states():
    """returning the all the obj from our db having state as class"""
    val = [object.to_dict() for object in storage.all(State).values()]
    return jsonify(val)

@app_views.route("/states/<state_id>", methods=['GET'])
def states_with_id(state_id):
    """getting the object with class state and particular id"""
    if not State:
        abort(404)
    state_element = storage.get(State, state_id)
    return jsonify(state_element.to_dict())

@app_views.route("/states/<state_id>", methods=['DELETE'])
def delete_with_id(state_id):
    """deletes states with a specific id"""
    if not state_id:
        abort(404)
    del_id = storage.delete(state_id)
    return jsonify(del_id.to_dict(), 200)

@app_views.route("/states", methods=['POST'])
def create_state():
    """creates a new state"""
    if not request.get_json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json:
        return jsonify({"error": "Missing name"}), 400
    new_object = State(**request.get_json())
    new_object.save()
    return make_response(jsonify(new_object.to_dict()), 201)

@app_views.route("/state/<state_id>", methods=["PUT"])
def update_state(state_id):
    """update a new state"""
    state = storage.all(State, id)
    if not state_id:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"})
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
        state.save()
    return make_response(jsonify(state.to_dict()), 200)