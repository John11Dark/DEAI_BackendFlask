from typing import Final
from bson import ObjectId
from datetime import datetime
from .Helpers import connect
from .Users import User


class Conversation:
    BOT_ID: Final = "60f1b5b3e3b3f3b3f3b3f3b3"

    def __init__(self, id):
        self.id = id

    # * --> Static Methods
    @staticmethod
    def conversations() -> list:
        """
        Get the conversations collection from the database.

        Returns:
            _pymongo.collection.Collection:   The conversations collection Object address in memory.
            _None_:  If an error occurred.
        """
        try:
            return connect("conversations")
        except Exception as e:
            return None

    @classmethod
    def get_conversation(cls, id: str | ObjectId) -> dict | None:
        """
        _summary_: Gets a conversation from the database

        Args:
            id (str | ObjectId): The id of the conversation to be retrieved

        Returns:
            _dict_: The conversation if it was found
            _None_: If the conversation was not found
        """

        if type(id) == str:
            id = ObjectId(id)
        conversations = cls.conversations()
        conversation = conversations.find_one({"_id": ObjectId(id)})
        if conversation is not None and conversation["_id"] == id:
            return conversation
        return None

    @classmethod
    def create_conversation(
        cls,
        conversation_id: str | ObjectId,
        sender: User,
    ) -> str | ObjectId | None:
        """
        _summary_: Creates a new conversation

        Args:
            conversation_id (str | ObjectId): The id of the conversation to be created
            sender (User): The user who created the conversation

        Returns:
            _str | ObjectId_: The id of the created conversation
            _None_: If an error occurred
        """

        if type(conversation_id) == str:
            conversation_id = ObjectId(conversation_id)

        conversation = cls.get_conversation(conversation_id)
        if conversation is not None:
            return str(conversation["_id"])
        else:
            conversations_collection = cls.conversations()
            new_conversation = {
                "title": "New Chat",
                "hasUnreadMessages": False,
                "hasNewTitle": False,
                "messages": [],
                "sentimentType": None,
                "lastMessage": None,
                "createdAt": str(datetime.utcnow()),
                "updatedAt": str(datetime.utcnow()),
                "avatar": "/assets/images/logo-icon.png",
                "sender": sender,
                "receiver": cls.BOT_ID,
            }
            try:
                response = conversations_collection.insert_one(new_conversation)
                if response.acknowledged:
                    return str(response.inserted_id)
                return None
            except Exception as e:
                return None

    @classmethod
    def get_messages_collection(cls):
        """
        _summary_: Gets the messages collection from the database

        Returns:
            _list_: The messages collection
            _None_: If an error occurred
        """
        db = connect("conversations")
        messages = db.find_one({"_id": ObjectId(cls.id)})
        return messages

    @classmethod
    def append_message(cls, message: dict) -> bool | None:
        """
        _summary_: Adds a message to the database

        Args:
            message (dict): The message to be added to the database

        Returns:
            _bool_: True if the message was added successfully, False otherwise
            _None_: None if an error occurred
        """
        conversation = cls.get_conversation(message["conversation_id"])
        try:
            if conversation is not None:
                response = conversation.insert_one(message)
                if response.acknowledged:
                    return True
            return None
        except Exception as e:
            return None

    @classmethod
    def delete_conversation(cls, id: str | ObjectId) -> bool | None:
        """
        _summary_: Deletes a conversation from the database

        Args:
            id (str | ObjectId): The id of the conversation to be deleted

        Returns:
            _bool_: True if the conversation was deleted successfully, False otherwise
            _None_: None if an error occurred
        """

        if type(id) == str:
            id = ObjectId(id)
        conversations = cls.conversations()
        try:
            response = conversations.delete_one({"_id": ObjectId(id)})
            if response.acknowledged and response.deleted_count > 0:
                return True
            return None
        except Exception as e:
            return None

    @classmethod
    def update_conversation(cls, id: str | ObjectId, data: dict) -> bool | None:
        """
        _summary_: Updates a conversation in the database

        Args:
            id (str | ObjectId): The id of the conversation to be updated
            data (dict): The data to be updated
        Returns:
            _bool_: True if the conversation was updated successfully, False otherwise
            _None_: None if an error occurred
        """
        if type(id) == str:
            id = ObjectId(id)
        conversations = cls.conversations()
        try:
            data["updatedAt"] = str(datetime.utcnow())
            response = conversations.find_one_and_update(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if response != None:
                return True
            return None
        except Exception as e:
            return None
