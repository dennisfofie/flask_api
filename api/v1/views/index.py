#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status_of_response():
    return jsonify({"status": "ok"})

@app_views.route('/stats')
def reading_stats():
    """return stats about the class"""
    return jsonify({"stats": storage.count()})

