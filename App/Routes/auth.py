from flask import jsonify, request
from datetime import datetime, timedelta
from ..Store import Users

from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    print(request.json["email"])
    return jsonify({"message": "Login successful"})


@auth.route("/register", methods=["POST"])
def register(userInfo, req):
    return jsonify({"message": "Register"})


@auth.route("/logout", methods=["POST"])
def logout(req):
    return jsonify({"message": "Logout"})
