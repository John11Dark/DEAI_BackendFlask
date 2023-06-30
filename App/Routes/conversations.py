from datetime import datetime
from flask import jsonify, request, Blueprint
from flask_socketio import SocketIO, emit
from ..Store.Conversations import Conversation
from ..Store.Helpers import JSONEncoder
from ..Store.Users import User

conversations = Blueprint("conversations", __name__)


@conversations.route("", methods=["GET", "POST"])
def users_route():
    if request.method == "GET":
        return jsonify({"conversations": get_conversations()}), 201
    elif request.method == "POST":
        data = request.get_json()
        return (
            jsonify(
                {
                    "message": "New conversation has been created successfully",
                    "id": create_conversation(data),
                }
            ),
            201,
        )


@conversations.route("/<query>", methods=["PUT", "DELETE", "GET"])
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


def get_conversations():
    conversations = list(Conversation.conversations())
    conversations = JSONEncoder().encode(conversations)
    return conversations


def create_conversation(data: dict) -> dict:
    user = data["sender"]
    id = data["conversation_id"]
    conversation = Conversation.create_conversation(
        conversation_id=id,
        sender=user,
    )
    try:
        JSONEncoder().encode(conversation)
    except:
        conversation["_id"] = str(conversation["_id"])
        conversation["updatedAt"] = str(conversation["updatedAt"])
        conversation["createdAt"] = str(conversation["createdAt"])
        conversation = JSONEncoder().encode(conversation)
    return conversation
