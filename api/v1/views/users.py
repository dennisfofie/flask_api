#!/usr/bin/python3
"""getting users data"""

from flask import request, make_response, jsonify, abort
from models import storage
from models.user import User
from api.v1.views import app_views

@app_views.route("/users", methods=['GET'])
def get_all_users():
    """getting all users from the database"""
    user = storage.all('User')
    return jsonify(user.to_dict())

@app_views.route("/users/<user_id>", methods=['GET'])
def get_specific_user(user_id):
    """get the user by using it id"""
    user = storage.get(user_id, User)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete a specific user"""
    user = storage.get(user_id, User)
    if not user:
        abort(404)
    user.delete()
    user.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'])
def create_user():
    """creates a new user"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 404)
    if not "name" in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 404)
    new_user = User(**request.get_json())
    new_user.save()
    return jsonify(new_user.to_dict()), 201

@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """updating a existing user"""
    user = storage.get(user_id, User)
    if not user:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not JSON"}), 404)
    for key, value in request.get_json().items():
        if key not in ["id", "email","created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200