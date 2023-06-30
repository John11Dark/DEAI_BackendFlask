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


@conversations.route("/<id>", methods=["PUT", "DELETE", "GET"])
def conversation(id):
    conversation = get_conversation(id)
    if conversation == None:
        return jsonify({"error": "User not found"}), 404
    else:
        if request.method == "GET":
            return jsonify({"data": conversation})
        elif request.method == "PUT":
            return {"data": "Conversation updated successfully"}
        elif request.method == "DELETE":
            response = {"message": "Conversation deleted successfully"}
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
    return conversation


def get_conversation(id: str) -> dict | None:
    conversation = Conversation.get_conversation(id)
    try:
        conversation = JSONEncoder().encode(conversation)
        if conversation is not None:
            return conversation
    except Exception as _:
        conversation["_id"] = str(conversation["_id"])
        conversation["updatedAt"] = str(conversation["updatedAt"])
        conversation["createdAt"] = str(conversation["createdAt"])
        conversation = JSONEncoder().encode(conversation)
        return conversation
    return None
