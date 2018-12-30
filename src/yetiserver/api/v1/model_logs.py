import traceback

from flask import Blueprint, make_response, request, current_app, jsonify
from yetiserver.api.v1.utils import authenticate_user

model_logs_blueprint = Blueprint('model_logs', __name__)


@model_logs_blueprint.route('/<user_name>/<model_name>/number_of_predictions/')
def number_of_predictions(user_name, model_name):
    try:
        if not authenticate_user(user_name, request):
            return make_response("Authentication failed", 403)
        counter = current_app.model_log.retrieve_predictions_counter(user_name, model_name)
        return jsonify(counter)
    except:
        traceback.print_exc()