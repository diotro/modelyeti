from flask import Blueprint, request, current_app, jsonify, abort, make_response

from yetiserver import authentication

user_management_blueprint = Blueprint('user', __name__)


@user_management_blueprint.route("/user/register/", methods=["POST"])
def register_user():
    json_body = request.get_json(force=True)
    if not isinstance(json_body, dict):
        return abort(500)

    try:
        username = json_body["username"]
        passhash = json_body["passhash"]
        user_email = json_body["user_email"]
    except KeyError:
        return abort(500)

    user_manager = current_app.auth
    user_manager.register_user(username, user_email, passhash)
    return jsonify(200)

