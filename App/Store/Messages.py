from datetime import datetime


class Message:
    """
    _summary_: Message class to represent a message sent by a user in a conversation

    Args:
        content (dict): The content of the message
        sender (str): The user id who sent the message
        timestamp (datetime): The time the message was sent
    """

    def __init__(self, content: dict, sender: str, timestamp: datetime):
        self.content = content
        self.sender = sender
        self.timestamp = timestamp

    @classmethod
    def to_dict(cls: dict) -> dict:
        """
        _summary_: Converts the message object to a dictionary

        Returns:
            _dict_: The dictionary representation of the message object
        """
        return {
            "content": cls.content,
            "sender": cls.sender,
            "timestamp": cls.timestamp,
        }

    @classmethod
    def from_dict(cls, message_dict: dict) -> dict:
        """
        _summary_: Converts a dictionary to a message object

        Returns:
            _dict_: The dictionary representation of the message object
        """
        return cls(
            content=message_dict.get("content"),
            sender=message_dict.get("sender"),
            timestamp=message_dict.get("timestamp"),
        )

    def __repr__(self):
        """_summary_: Representation of the message object

        Returns:
            _string_: The string representation of the message object
        """
        return f"<id: {self.content.get('id')},  Message: {self.content.get('message')}, time: {self.content.get('time')}>"
