from flask import jsonify, request, Blueprint
from ..Store.Users import User

users = Blueprint("users", __name__)


@users.route("/users", methods=["POST", "GET"])
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


@users.route("/users/<id>", methods=["PUT", "DELETE", "GET"])
def user(id):
    if request.method == "GET":
        return get_user(id)
    elif request.method == "PUT":
        return update_user(id, request.get_json())
    elif request.method == "DELETE":
        return delete_user(id)


# * --> Helper Functions


def get_user(id):
    return jsonify(User.get_user_by_id(id))


def create_user(data):
    return jsonify(User.create_user(**data))


def update_user(id, data):
    return jsonify(User.update_user(id, **data))


def delete_user(id):
    return jsonify(User.delete_user(id))


def get_users():
    return jsonify(User.get_all_users())
