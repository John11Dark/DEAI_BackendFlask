from flask import jsonify, request, Blueprint

platforms = Blueprint("platforms", __name__)


@platforms.route("", methods=["GET", "POST"])
def conversations_route():
    if request.method == "GET":
        return jsonify({"platforms": "There are no connected platforms"}), 201
    elif request.method == "POST":
        return (
            jsonify(
                {
                    "message": "New platform has been created successfully",
                }
            ),
            201,
        )


@platforms.route("/<id>", methods=["PUT", "DELETE", "GET"])
def conversation(id):
    if request.method == "GET":
        return jsonify({"data": "There are no connected platforms"})
    elif request.method == "PUT":
        return jsonify({"message": "Platform updated successfully"}), 200
    elif request.method == "DELETE":
        return jsonify({"message": "Platform deleted successfully"}), 200
    else:
        return jsonify({"error": "Method not allowed"}), 405
