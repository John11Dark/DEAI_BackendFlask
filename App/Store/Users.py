# * --> Imports
import os
import bcrypt
from datetime import datetime, timedelta
from bson import ObjectId
import jwt
from .Helpers import connect


# * --> User Class
class User:
    """Represents a user in the system."""

    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        password: str,
        country_code: str,
        phone_number: int,
        address: dict,
        role: str,
        verified: bool,
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
        self.country_code = country_code
        self.phone_number = phone_number
        self.address = address
        self.role = role
        self.created_at = datetime.utcnow()
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
    def encrypt_password(password: str):
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
    def decrypt_password(hashed_password: str, password: str):
        """
        Check if the provided password matches the hashed password.

        Args:
            hashed_password (str): The hashed password stored in the database.
            password (str): The password to check.

        Returns:
            bool: True if the passwords match, False otherwise.

        """

        return bcrypt.checkpw(password.encode(), hashed_password.encode())  # type: ignore

    @staticmethod
    def generate_token(user: dict):
        """
        Generate a JWT token for the user.

        Args:
            user (str): The user identifier.

        Returns:
            str: The generated JWT token.

        """
        try:
            SECRET_KEY = os.getenv("SECRET_KEY")
            expiration_time = datetime.utcnow() + timedelta(days=7)
            # ! * --> 7 days expiration
            payload = {
                "id": str(user["_id"]),
                "name": user["name"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
                "date_joined": str(user["created_at"]),
                "exp": expiration_time,
                "iat": datetime.utcnow(),
            }
            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm="HS256",
            )

            return token
        except Exception as e:
            return None

    @staticmethod
    def decode_token(token: str):
        """
        Decode the JWT token.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded token if successful, None otherwise.

        """
        try:
            SECRET_KEY = os.getenv("SECRET_KEY")
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded_token
        except Exception as e:
            return None

    @staticmethod
    def verify_token(token: str):
        """
        Verify the JWT token.

        Args:
            token (str): The JWT token to verify.

        Returns:
            bool: True if the token is valid, False otherwise.

        """
        try:
            SECRET_KEY = os.getenv("SECRET_KEY")
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return True
        except Exception as e:
            return False

    @staticmethod
    def verify_password(req_password: str, db_password: str):
        """
        Verify the password.

        Args:
            req_password (str): The password provided in the request.
            db_password (str): The password stored in the database.

        Returns:
            bool: True if the passwords match, False otherwise.

        """
        return bcrypt.checkpw(req_password.encode(), db_password.encode())

    @staticmethod
    def verify_admin(self, headers, id):
        """
        Verify if a user is an admin.

        Args:
            headers (dict): The request headers containing the authorization information.
            id (str): The ID of the user.

        Returns:
            bool: True if the user is an admin, False otherwise.

        """
        return True

    @classmethod
    def login_user(cls, data):
        user = cls.get_user_by_email(data["email"])
        if user != None:
            if cls.verify_password(data["password"], user["password"]):
                token = cls.generate_token(user)
                return token
            else:
                return {"error": "invalid credentials"}
        else:
            return {"error": "invalid credentials"}

    @classmethod
    def logout_user(cls, data):
        # ! need to implement
        return True

    # * --> Class Methods
    @classmethod
    def create_user(
        self,
        username,
        name,
        email,
        password,
        phone_number,
        role,
    ):
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
        users_collection = self.users()
        hashed_password = self.encrypt_password(password)
        user_data = {
            "username": username,
            "name": name,
            "email": email,
            "password": hashed_password,
            "phone_number": phone_number,
            "role": role,
            "created_at": datetime.utcnow(),
        }
        existing_user = users_collection.find_one(
            {
                "$or": [
                    {"email": email},
                    {"phone_number": phone_number},
                    {"username": username},
                ]
            }
        )
        if (
            existing_user == None
            or existing_user == {}
            or existing_user == []
            or existing_user == "null"
            or existing_user == ""
        ):
            try:
                result = users_collection.insert_one(user_data)
                if result != None:
                    return result.inserted_id
                else:
                    return {"error": "unable to create user"}
            except Exception as _:
                return {"error": "something went wrong"}
        else:
            return {"error": "user already exists"}

    @classmethod
    def update_user(
        self, user_id, name, email, verified, password, phone_number, address, role
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
        users_collection = self.users()
        query = {"_id": user_id}
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
        try:
            result = users_collection.update_one(query, new_values)
        except Exception as _:
            return 0
        return result.modified_count

    @classmethod
    def delete_user(self, user_id):
        """
        Delete a user.

        Args:
            user_id (str): The ID of the user to delete.

        Returns:
            int: The number of deleted documents (should be 1).

        """
        users_collection = self.users()
        query = {"_id": user_id}
        try:
            result = users_collection.delete_one(query)
        except Exception as _:
            return 0
        return result.deleted_count

    @classmethod
    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            dict: The user document.

        """
        users_collection = self.users()
        query = {"_id": user_id}
        try:
            user = users_collection.find_one(query)
        except Exception as _:
            return None
        return user

    @classmethod
    def get_all_users(self):
        """
        Retrieve all users.

        Returns:
            list: A list of all user documents.

        """
        users_collection = self.users()
        try:
            all_users = users_collection.find()
        except Exception as _:
            return None
        return list(all_users)

    @classmethod
    def get_user_by_email(self, email):
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            dict: The user document.

        """
        users_collection = self.users()
        query = {"email": email}
        try:
            user = users_collection.find_one(query)
        except Exception as _:
            return None
        return user

    @classmethod
    def get_user_by_username(self, username):
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            dict: The user document.

        """
        users_collection = self.users()
        query = {"username": username}
        try:
            user = users_collection.find_one(query)
        except Exception as _:
            return None
        return user

    @classmethod
    def get_user_by_phone_number(self, phone_number):
        """
        Retrieve a user by their phone number.

        Args:
            phone_number (str): The phone number of the user to retrieve.

        Returns:
            dict: The user document.

        """
        users_collection = self.users()
        query = {"phone_number": phone_number}
        try:
            user = users_collection.find_one(query)
        except Exception as _:
            return None
        return user

    @classmethod
    def register_user(self, **data):
        user_id = self.create_user(**data)
        if user_id != None and type(user_id) != dict:
            user = self.get_user_by_id(ObjectId(user_id))
            token = self.generate_token(user)
            if token != None and type(token) != dict:
                return token
            else:
                return {"message": "unable to generate token"}
        else:
            return user_id
