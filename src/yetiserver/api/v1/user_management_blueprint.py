from functools import wraps

from flask import Blueprint, request, current_app, jsonify, abort, make_response

user_management_blueprint = Blueprint('user', __name__)


def uses_json_keys(*keys):
    """Provides the specified json keys as keyword args to the
    given function. aborts with 500 if the keys don't exist in the json body
    of the request being handled."""

    # The decorator function: given a handler that we want to add
    # key retrieval to, will pass kwargs for those keys.
    def decorator(func):
        # This returns the wrapped function, which will first perform
        # the validation, then retrieve the key/value pairs from the json
        # body of the current request, and then provide those values as kwargs
        # to the provided handler function.
        @wraps(func)
        def wrapper(*args, **kwargs):
            # This code used to exist in each handler, but now can be deduplicated and
            # only maintained here: retriving the json body, ensuring the
            # right keys exist, and then extracting values for the needed keys.
            json_body = request.get_json(force=True)
            if not ensure_json_is_dictionary_with_keys(json_body, *keys):
                abort(500)
            else:
                retrieved = {key: json_body[key] for key in keys}
                return func(*args, **kwargs, **retrieved)

        return wrapper

    return decorator

def ensure_json_is_dictionary_with_keys(value, *required_keys):
    if not isinstance(value, dict):
        return False

    for key in required_keys:
        if key not in value:
            return False

    return True


@user_management_blueprint.route("/user/register/", methods=["POST"])
@uses_json_keys("username", "passhash", "email")
def register_user(username, passhash, email):
    """Registers a user. Requires a json dict to be POSTed, containing the keys
    "username", "passhash", and "user_email".

    :return: 200 is successful, 500 if failure
    """
    user_manager = current_app.auth
    user_manager.register_user(username, email, passhash)
    return jsonify(200)


@user_management_blueprint.route("/user/info/", methods=["GET"])
@uses_json_keys("username", "passhash")
def info(username, passhash):
    user_manager = current_app.auth

    if user_manager.check_credentials(username, passhash):
        return jsonify(user_manager.user_info(username))
    else:
        return abort(500)


@user_management_blueprint.route("/user/change_password/", methods=["POST"])
@uses_json_keys("username", "old_password", "new_password")
def change_password(username, old_password, new_password):
    user_manager = current_app.auth

    if user_manager.check_credentials(username, old_password):
        user_manager.update_password(username, new_password)
        return jsonify(200)
    else:
        return abort(500)


@user_management_blueprint.route("/user/update_email/", methods=["POST"])
@uses_json_keys("username", "passhash", "new_email")
def update_email(username, passhash, new_email):
    """Updates the email of the given user."""
    user_manager = current_app.auth
    if user_manager.check_credentials(username, passhash):
        user_manager.update_email(username, new_email)
        return jsonify(200)
    else:
        return abort(500)


@user_management_blueprint.route("/user/delete/", methods=["DELETE"])
@uses_json_keys("username", "passhash")
def delete_user(username, passhash):
    """Deletes a user. Expects a JSON dict to be included, containing the keys "username" and
    "passhash".

    :return: 500 if the request failed, 200 if the user is deleted
    """
    user_manager = current_app.auth
    if user_manager.check_credentials(username, passhash):
        user_manager.delete_user(username)
        return jsonify(200)
    else:
        return abort(500)

