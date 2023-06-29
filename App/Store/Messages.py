from datetime import datetime
from ..Store.Users import User
from ..Store.Conversations import Conversation
from flask import Blueprint, jsonify, request
from ..Store.Helpers import JSONEncoder


class Message:
    def __init__(self, content, sender, timestamp):
        self.content = content
        self.sender = sender
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "content": self.content,
            "sender": self.sender,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, message_dict):
        return cls(
            content=message_dict.get("content"),
            sender=message_dict.get("sender"),
            timestamp=message_dict.get("timestamp"),
        )
