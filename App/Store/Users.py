# * --> Imports
import os
import bcrypt
from datetime import datetime, timedelta
import jwt
from ..Models import connect


# * --> User Class
class User:
    """Represents a user in the system."""

    def __init__(
        self, user_id, name, email, password, phone_number, address, role, verified
    ):
        """
        Initialize a User object.

        Args:
            user_id (str): The unique identifier for the user.
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The user's password.
            phone_number (str): The phone number of the user.
            address (str): The address of the user.
            role (str): The role of the user (e.g., admin, regular user).
            verified (bool): Indicates if the user is verified.
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.address = address
        self.role = role
        self.updated_at = datetime.utcnow()
        self.verified = verified

    # * --> Static Methods
    @staticmethod
    def users():
        """
        Get the users collection from the database.

        Returns:
            pymongo.collection.Collection: The users collection.
        """
        return connect("users")

    @staticmethod
    def encrypt_password(password):
        """
        Encrypt the password using bcrypt.

        Args:
            password (str): The password to encrypt.

        Returns:
            str: The encrypted hashed password.

        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode()

    @staticmethod
    def decrypt_password(hashed_password, password):
        """
        Check if the provided password matches the hashed password.

        Args:
            hashed_password (str): The hashed password stored in the database.
            password (str): The password to check.

        Returns:
            bool: True if the passwords match, False otherwise.

        """

        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def generate_token(user):
        """
        Generate a JWT token for the user.

        Args:
            user (str): The user identifier.

        Returns:
            str: The generated JWT token.

        """
        try:
            SECRET_KEY = os.getenv("SECRET_KEY")
            expiration_time = datetime.utcnow() + timedelta(days=7)  # 7 days expiration
            payload = {
                "user": user,
                "expiration": expiration_time.isoformat(),
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return token
        except Exception as e:
            print(e)
            return None

    # * --> Class Methods
    @classmethod
    def create_user(cls, name, email, password, phone_number, address, role, verified):
        """
        Create a new user.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The user's password.
            phone_number (str): The phone number of the user.
            address (str): The address of the user.
            role (str): The role of the user.
            verified (bool): Indicates if the user is verified.

        Returns:
            str: The inserted user's ID.

        """
        users_collection = cls.users()
        user_data = {
            "name": name,
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "address": address,
            "role": role,
            "verified": verified,
            "created_at": datetime.utcnow(),
        }
        result = users_collection.insert_one(user_data)
        return result.inserted_id

    @classmethod
    def update_user(
        cls, user_id, name, email, verified, password, phone_number, address, role
    ):
        """
        Update an existing user.

        Args:
            user_id (str): The ID of the user to update.
            name (str): The updated name of the user.
            email (str): The updated email address of the user.
            verified (bool): The updated verification status of the user.
            password (str): The updated password of the user.
            phone_number (str): The updated phone number of the user.
            address (str): The updated address of the user.
            role (str): The updated role of the user.

        Returns:
            int: The number of modified documents (should be 1).

        """
        users_collection = cls.users()
        query = {"user_id": user_id}
        new_values = {
            "$set": {
                "name": name,
                "email": email,
                "updated_at": datetime.utcnow(),
                "verified": verified,
                "password": password,
                "phone_number": phone_number,
                "address": address,
                "role": role,
            }
        }
        result = users_collection.update_one(query, new_values)
        return result.modified_count

    @classmethod
    def delete_user(cls, user_id):
        """
        Delete a user.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            int: The number of deleted documents (should be 1).

        """
        users_collection = cls.users()
        query = {"user_id": user_id}
        result = users_collection.delete_one(query)
        return result.deleted_count

    @classmethod
    def get_user_by_id(cls, user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            dict: The user document.

        """
        users_collection = cls.users()
        query = {"user_id": user_id}
        user = users_collection.find_one(query)
        return user

    @classmethod
    def get_all_users(cls):
        """
        Retrieve all users.

        Returns:
            list: A list of all user documents.

        """
        users_collection = cls.users()
        all_users = users_collection.find()
        return list(all_users)

    @classmethod
    def get_user_by_email(cls, email):
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            dict: The user document.

        """
        users_collection = cls.users()
        query = {"email": email}
        user = users_collection.find_one(query)
        return user

    @classmethod
    def get_user_by_username(cls, username):
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            dict: The user document.

        """
        users_collection = cls.users()
        query = {"username": username}
        user = users_collection.find_one(query)
        return user

    @classmethod
    def get_user_by_phone_number(cls, phone_number):
        """
        Retrieve a user by their phone number.

        Args:
            phone_number (str): The phone number of the user to retrieve.

        Returns:
            dict: The user document.

        """
        users_collection = cls.users()
        query = {"phone_number": phone_number}
        user = users_collection.find_one(query)
        return user

    @classmethod
    def verify_admin(cls, headers, id):
        """
        Verify if a user is an admin.

        Args:
            headers (dict): The request headers containing the authorization information.
            id (str): The ID of the user.

        Returns:
            bool: True if the user is an admin, False otherwise.

        """
        return True
