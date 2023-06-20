from dotenv import load_dotenv
from flask import Flask
import os

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.after_request
def set_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


from App.Routes import index, users, auth

app.register_blueprint(index.views, url_prefix="/")
app.register_blueprint(auth.auth, url_prefix="/auth")
app.register_blueprint(users.users, url_prefix="/users")
# app.register_blueprint(platforms.platforms, url_prefix="/platforms")
# app.register_blueprint(messages.messages, url_prefix="/messages")
