# This file contains the unit tests for the API

import requests
import os

server_url = os.getenv("SERVER_URL")


# Test Post  Endpoint
def test_post_Method(endpoint, data):
    response = requests.post(endpoint, data=data)
    assert response.status_code == 201


# Test Get  Endpoint
def test_get_Method(endpoint):
    response = requests.get(server_url + endpoint)
    assert response.status_code == 200


# Test Put  Endpoint
def test_put_Method(endpoint, id, data):
    response = requests.put({"server_url, endpoint, ": ""}, id, data=data)
    assert response.status_code == 200


# Test Delete  Endpoint
def test_delete_Method(endpoint, id):
    response = requests.delete(endpoint, ":", id)
    assert response.status_code == 204


# Test User Post  Endpoint
test_user = {
    "username": "test",
    "password": "test",
    "email": "test@mail.com",
    "name": "test",
    "age": 20,
    "role": "user",
    "avatar": "test",
    "phoneNumber": "00001111",
    "countryCode": "+356",
    "verified": False,
    "gender": True,
}

responseUser = test_post_Method("users/", test_user)
print(responseUser)

# Test Users Get  Endpoint
responseUsers = test_get_Method("users/")
print(responseUsers)

# Test Single User Get  Endpoint
responseSingleUser = test_get_Method("users/", responseUser["id"])
print(responseSingleUser)

# Test User Put  Endpoint
test_user = {"username": "updated name", "password": "updated password"}

responseUpdatedUser = test_put_Method("users/", responseUser["id"], test_user)
print(responseUpdatedUser)

# Test User Delete  Endpoint
responseDeletedUser = test_delete_Method("users/", responseUser["id"])
print(responseDeletedUser)

# Test Conversation Post  Endpoint
