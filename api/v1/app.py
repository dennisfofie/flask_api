#!/usr/bin/python3
""" creating a blueprint """

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_app():
    storage.close()

@app.errorhandler(404)
def handle_404(error):
    """handles 404 error page"""
    return make_response(jsonify({"error": "Not Found"}), 404)



if __name__ == "__main__":
    app.run(threaded=True, debug=True)
