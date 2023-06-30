from bson import ObjectId
from datetime import datetime
from .Helpers import connect
from .Messages import Message
from .Users import User
from ..Utils.SentimentAnalyzer import SentimentAnalyzer


class Conversation:
    def __init__(self, id):
        self.id = id
        self.sentimentAnalyzer = SentimentAnalyzer()

    # * --> Static Methods
    @staticmethod
    def conversations() -> list:
        """
        Get the conversations collection from the database.

        Returns:
            _list:   The conversations collection. (pymongo.collection.Collection: parsed into a list)
            _None_:  If an error occurred.
        """
        try:
            return connect("conversations")
        except Exception as e:
            return None

    def get_conversation(self, id: str | ObjectId) -> dict | None:
        if type(id) == str:
            id = ObjectId(id)
        conversations = self.conversations()
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
        if type(conversation_id) == str:
            conversation_id = ObjectId(conversation_id)

        conversation = cls.get_conversation(conversation_id)
        if conversation is not None:
            print("Conversation already exists")
            return conversation
        else:
            print("Creating new conversation")
            conversations_collection = cls.conversations()
            new_conversation = {
                "title": "New Chat",
                "hasUnreadMessages": False,
                "hasNewTitle": False,
                "messages": [],
                "sentimentType": "null",
                "lastMessage": "null",
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow(),
                "user": sender,
                "avatar": "/assets/images/logo-icon.png",
            }
            try:
                response = conversations_collection.insert_one(new_conversation)
                if response.acknowledged:
                    return response.inserted_id
                return None
            except Exception as e:
                return None

    @classmethod
    def get_messages_collection(cls):
        db = connect("conversations")
        messages = db.find_one({"_id": ObjectId(cls.id)})
        return messages

    @classmethod
    def add_message(cls, message: dict) -> bool | None:
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
            response = conversation.insert_one(message)
            if response.acknowledged:
                return True
        except Exception as e:
            return None

    @classmethod
    def get_conversation(cls, conversation_id: str | ObjectId) -> dict | None:
        db = connect("conversations")
        conversation = db.find_one({"_id": ObjectId(conversation_id)})
        return conversation
