from flask import jsonify, request, Blueprint
from flask_socketio import SocketIO, emit
from ..Store.Conversations import Conversation
from ..Store.Helpers import JSONEncoder

conversations = Blueprint("conversations", __name__)


@conversations.route("", methods=["GET", "POST"])
def conversations_route():
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
            data = request.get_json()
            result = Conversation.update_conversation(id, data)
            if result:
                return jsonify({"message": "Conversation updated successfully"}), 200
            return jsonify({"error": "Conversation not found"}), 404
        elif request.method == "DELETE":
            result = Conversation.delete_conversation(id)
            if result == None:
                return (
                    jsonify(
                        {
                            "error": "Conversation not found",
                            "message": "Something went wrong! make sure that the id is correct and the conversation exist try to reload your page",
                        }
                    ),
                    404,
                )
            else:
                return jsonify({"message": "Conversation deleted successfully"}), 200


# * --> Helper Functions


def get_conversations() -> dict | None:
    """
    _summary_: Gets all conversations from the database

    Returns:
        _dict_: A dictionary containing all conversations
        _None_: None if an error occurred
    """

    conversations_collection = Conversation.conversations()
    conversations_collection = list(conversations_collection.find())

    try:
        response = JSONEncoder().encode(conversations_collection)
        if response is not None:
            return response
    except Exception as _:
        for conversation in conversations_collection:
            conversation["_id"] = str(conversation["_id"])
            conversation["updatedAt"] = str(conversation["updatedAt"])
            conversation["createdAt"] = str(conversation["createdAt"])
        response = JSONEncoder().encode(conversations_collection)
        if response is not None:
            return response
    return None


def create_conversation(data: dict) -> dict:
    """
    _summary_: Creates a new conversation

    Args:
        data (dict): The data of the conversation to be created

    Returns:
        _dict_: The id of the created conversation
    """
    user = data["sender"]
    id = data["conversation_id"]
    conversation = Conversation.create_conversation(
        conversation_id=id,
        sender=user,
    )
    return conversation


def get_conversation(id: str) -> dict | None:
    """
    _summary_: Gets a conversation from the database

    Args:
        id (str): The id of the conversation to be retrieved

    Returns:
        _dict_: The conversation if it was found
        _None_: If the conversation was not found
    """
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
