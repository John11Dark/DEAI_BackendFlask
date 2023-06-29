from flask import jsonify, request
from datetime import datetime, timedelta
from ..Store.Users import User

from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    login_credentials = request.get_json()["login_credentials"]
    token = User.login_user(login_credentials)
    if token != None:
        if type(token) == str:
            return jsonify(token)
        else:
            return (
                jsonify({"message": "invalid credentials"}),
                401,
            )
    return jsonify({"message": "Login failed"}), 401


@auth.route("/register", methods=["POST"])
def register():
    userInfo = request.get_json()["register_credentials"]

    token = User.register_user(**userInfo)
    if token != None and type(token) == str:
        return jsonify(token), 201
    return jsonify({"header": "Registration failed", "data": token}), 400


@auth.route("/logout", methods=["POST"])
def logout():
    # data = request.get_json()["logout_credentials"]
    data = {"token": "request.headers"}  # ! need to implement logout
    res = User.logout_user(**data)
    if res != None:
        return jsonify({"message": "user logged out successfully"})
    else:
        return jsonify({"message": "something went wrong could not log out user"})
