#!/usr/bin/python3
"""looking for each amenities at a particular place"""

from flask import request, make_response, abort, jsonify
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

@app_views.route("/amenities", methods=['GET'])
def get_all_amenities():
    """retrieve all the amenities object"""
    amenity = storage.all('Amenity')
    return jsonify(amenity.to_dict()), 200

@app_views.route("/amenities/<amenity_id>", methods=['GET'])
def get_amenity_by_id(amenity_id):
    """gets a specific amenity using its id"""
    amenity = storage.get(amenity_id, Amenity)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200

@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete a specific amenity using the id"""
    amenity = storage.get(amenity_id, Amenity)
    if not amenity:
        abort(404)
    amenity.delete()
    amenity.save()
    return jsonify({}), 200

@app_views.route("/amenities")
def create_new_amenity():
    """adding new amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 404)
    if not "name" in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 404)
    new_amenity = Amenity(*request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict())

@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """update existing amenity"""
    amenity = storage.get(amenity_id, Amenity)
    if not amenity:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error":"Not a JSON"}), 404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key , value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200    