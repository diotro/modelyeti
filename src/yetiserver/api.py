"""A blueprint for the model management components of the API."""


from flask import Blueprint, current_app, request, jsonify, make_response

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/model/upload/<user_name>/<model_name>', methods=["POST"])
def upload_model(user_name, model_name):
    """Uploads a decision tree model with the given name"""
    if not current_app.auth.authenticate_user(user_name, request):
        return make_response("Authentication failed", 403)

    model_json = request.get_json(force=True)
    current_app.dao.store_model(user_name, model_name, model_json)
    return jsonify(success=True)


@api_blueprint.route('/model/<user_name>/<model_name>/predict/')
def predict_with_model(user_name, model_name):
    if not authenticate_user(user_name, request):
        return make_response("Authentication failed", 403)

    row = request.get_json(force=True)
    model_func = current_app.dao.retrieve_model(user_name, model_name)
    if model_func:
        return jsonify(model_func(row), success=True)
    else:
        resp = jsonify("No Such Model")
        resp.status_code = 404
        return resp


def authenticate_user(user_name, request):
    pass_hash = request.headers.get("password_hash_sha3_512")
    return current_app.auth.check_credentials(user_name, pass_hash)
