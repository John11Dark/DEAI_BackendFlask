from datetime import datetime
from connect import connect

db = connect("users")
user = {
    "name": "John",
    "username": "admin",
    "email": "info@johnmuller.eu",
    "password": "admin",
    "role": "admin",
    "created": str(datetime.utcnow()),
    "updated": str(datetime.utcnow()),
    "verified": False,
}

res = db.insert_one(user)

print("User created")
print(res)
