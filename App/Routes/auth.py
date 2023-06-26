from flask import jsonify, request
from datetime import datetime, timedelta
from ..Store.Users import User

from flask import Blueprint

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    print(request.get_json())
    login_credentials = request.get_json()["login_credentials"]
    token = User.login_user(login_credentials)
    if token != None:
        return jsonify(token)
    return jsonify({"message": "Login failed"}), 401


@auth.route("/register", methods=["POST"])
def register():
    userInfo = request.get_json()["register_credentials"]

    token = User.create_user("register", **userInfo)
    if token["value"] != None and token["error"] != False:
        return jsonify(token["value"]), 201
    return jsonify({"message": "Registration failed", "error": token}), 401


@auth.route("/logout", methods=["POST"])
def logout(req):
    res = logoutUser(req)
    if res != None:
        return jsonify({"message": "user logged out successfully"})
    else:
        return jsonify({"message": "something went wrong could not log out user"})


def logoutUser(req):
    return True
