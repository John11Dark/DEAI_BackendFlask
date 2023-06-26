from flask import jsonify, request, Blueprint
from ..Store.Users import User

users = Blueprint("users", __name__)

import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@users.route("", methods=["POST", "GET"])
def users_route():
    if User.verify_admin(
        request.headers.get("Authorization"), request.headers.get("user_id")
    ):
        if request.method == "GET":
            return jsonify({"users": get_users()})
        elif request.method == "POST":
            return create_user(request.get_json())
    else:
        return jsonify({"error": "Unauthorized"}), 401


@users.route("/<query>", methods=["PUT", "DELETE", "GET"])
def user(query):
    user = get_user_by_query(query)
    if user == None or user == "null" or user == "" or user == 0:
        return jsonify({"error": "User not found"}), 404
    else:
        if request.method == "GET":
            return jsonify(JSONEncoder().encode(user))
        elif request.method == "PUT":
            return update_user(user["_id"], request.get_json())
        elif request.method == "DELETE":
            response = delete_user(user["_id"])
            return jsonify({"data": response})


# * --> Helper Functions


def get_user_by_query(query: str) -> str:
    if query != None and query != "" and type(query) is str and "=" not in query:
        return None
    query_type = query.lower().split("=")[0]
    value = query.split("=")[1]
    if query_type not in ["id", "email", "phone_number", "username"] and value == "":
        return None
    user = None
    if query_type == "id":
        try:
            id = ObjectId(value)
            user = User.get_user_by_id(id)
        except Exception as _:
            return None
    elif query_type == "email":
        user = User.get_user_by_email(value)
    elif query_type == "phone_number":
        user = User.get_user_by_phone_number(value)
    elif query_type == "username":
        user = User.get_user_by_username(value)

    if user == None:
        return None
    return user


def create_user(data: dict) -> str:
    return JSONEncoder().encode(User.create_user(**data))


def update_user(id: str, data: dict) -> str:
    print(id)
    try:
        id = ObjectId(id)
    except Exception as _:
        return None
    return JSONEncoder.encode(User.update_user(id, **data))


def delete_user(id: str) -> str:
    try:
        id = ObjectId(id)
    except Exception as _:
        return None
    return JSONEncoder().encode(User.delete_user(id))


def get_users() -> str:
    return JSONEncoder().encode(User.get_all_users())
