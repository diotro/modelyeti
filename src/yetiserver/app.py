import datetime
import json

from yetiserver import dao
from yetiserver.logger import logging
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)


@app.route('/model/upload/<user_name>/<model_name>', methods=["POST"])
def upload_model(user_name, model_name):
    """Uploads a decision tree model with the given name"""
    model_json = request.get_json(force=True)

    information_to_log = {"url": request.url,
                          "model_json": model_json,
                          "user_name": user_name,
                          "model_name": model_name,
                          "time": datetime.datetime.now().timestamp(),
                          }
    logging.debug(f"request: {json.dumps(information_to_log)}")
    dao.store_model(user_name, model_name, model_json)
    return jsonify(success=True)


@app.route('/model/<user_name>/<model_name>/predict/')
def predict_with_model(user_name, model_name):
    row = request.get_json(force=True)

    information_to_log = {"url": request.url,
                          "input_data": row,
                          "user_name": user_name,
                          "model_name": model_name,
                          "time": datetime.datetime.now().timestamp(),
                          }
    logging.debug(f"request: {json.dumps(information_to_log)}")

    model_func = dao.retrieve_model(user_name, model_name)
    if model_func:
        return jsonify(model_func(row), success=True)
    else:
        resp = jsonify("No Such Model")
        resp.status_code = 404
        return resp
