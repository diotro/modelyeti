from flask import Blueprint, request, current_app, jsonify, abort, make_response

user_management_blueprint = Blueprint('user', __name__)


@user_management_blueprint.route("/user/register/", methods=["POST"])
def register_user():
    """Registers a user. Requires a json dict to be POSTed, containing the keys
    "username", "passhash", and "user_email".

    :return: 200 is successful, 500 if failure
    """
    json_body = request.get_json(force=True)
    if not ensure_json_is_dictionary_with_keys(json_body, "username", "passhash", "user_email"):
        return abort(500)

    username = json_body["username"]
    passhash = json_body["passhash"]
    user_email = json_body["user_email"]

    user_manager = current_app.auth
    user_manager.register_user(username, user_email, passhash)
    return jsonify(200)


@user_management_blueprint.route("/user/change_password/", methods=["POST"])
def change_password():
    json_body = request.get_json(force=True)
    if not ensure_json_is_dictionary_with_keys(json_body, "username", "old_password", "new_password"):
        return abort(500)

    username = json_body["username"]
    old_password = json_body["old_password"]
    new_password = json_body["new_password"]
    user_manager = current_app.auth

    if user_manager.check_credentials(username, old_password):
        user_manager.update_password(username, new_password)
        return jsonify(200)
    else:
        return abort(500)


@user_management_blueprint.route("/user/delete/", methods=["DELETE"])
def delete_user():
    """Deletes a user. Expects a JSON dict to be included, containing the keys "username" and
    "passhash".

    :return: 500 if the request failed, 200 if the user is deleted
    """
    json_body = request.get_json(force=True)
    if not ensure_json_is_dictionary_with_keys(json_body, "username", "passhash"):
        return abort(500)

    username = json_body["username"]
    passhash = json_body["passhash"]

    user_manager = current_app.auth
    if user_manager.check_credentials(username, passhash):
        user_manager.delete_user(username)
        return jsonify(200)
    else:
        return abort(500)


def ensure_json_is_dictionary_with_keys(value, *required_keys):
    if not isinstance(value, dict):
        return False

    for key in required_keys:
        if key not in value:
            return False

    return True
