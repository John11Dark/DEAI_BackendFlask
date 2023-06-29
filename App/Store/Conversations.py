from .Helpers import connect
from bson import ObjectId
from .Messages import Message


class Conversation:
    def __init__(self, id):
        self.id = id
        self.messages_collection = self.get_messages_collection()

    def get_messages_collection(self):
        db = connect("conversations")
        messages = db.find_one({"_id": ObjectId(self.id)})
        return messages["messages"]

    def add_message(self, message):
        message_data = message.to_dict()
        self.messages_collection.insert_one(message_data)

    def get_messages(self):
        messages = []
        cursor = self.messages_collection.find()
        for document in cursor:
            message = Message.from_dict(document)
            messages.append(message)
        return messages
