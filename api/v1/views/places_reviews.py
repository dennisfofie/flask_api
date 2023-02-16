#!/usr/bin/python3
"""reviews about a certain place"""

from flask import request, jsonify, abort
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views


@app_views.route("/reviews/<review_id>", methods=["GET", "PUT", "DELETE"])
def reviews_place(review_id):
    """get, update and delete reviews of a certain place"""
    review = storage.get(review_id, Review)
    if not review:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict()), 200
    
    if request.method == "DELETE":
        review.delete()
        review.save()
        return jsonify({}), 200
    
    if request.method == "PUT":
        if not request.get_json():
            abort(404, "Not a JSON")
        for key , value in request.get_json().items():
            if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    

@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def create_and_get(place_id):
    """adding a review and getting it"""
    place = storage.get(place_id, Place)

    if request.method == "POST":
        if not request.get_json():
            abort(404, "Not a JSon")
        if not place:
            abort(404)
        if not 'user_id' in request.get_json():
            abort(404, "Missing user_id")
        if not storage.get(request.get_json()['user_id'], "User"):
            abort(404)
        if not "text" in request.get_json():
            abort(404, "Missing text")
        new_review = Review(**request.get_json())
        new_review.place_id = place.place_id
        new_review.save()
        return (new_review.to_dict()), 201
    
    if request.method == "GET":
        if not place:
            abort(404)
        for view in place.reviews:
            return jsonify(view.to_dict())