from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.after_request
def set_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


from App.Routes import index, users, auth, conversations

app.register_blueprint(index.views, url_prefix="/")
app.register_blueprint(auth.auth, url_prefix="/auth")
app.register_blueprint(users.users, url_prefix="/users")
app.register_blueprint(conversations.conversations, url_prefix="/conversations")
# app.register_blueprint(platforms.platforms, url_prefix="/platforms")
