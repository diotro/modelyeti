import json

from flask import Flask, request, make_response
from model import DecisionTree
import redis

app = Flask(__name__)


def get_redis_connection():
    return redis.Redis(
        host='localhost',
        port=6379,
        password='')


redis_conn = get_redis_connection()


@app.route('/model/upload/decisiontree/<name>', methods=["POST"])
def upload_model(name):
    """Uploads a decision tree model with the given name"""
    model = DecisionTree(request.get_json(force=True))
    persist_model(name, model)
    return "OK"


def persist_model(name, model):
    redis_conn.set(name, json.dumps(model.data))


def retrieve_model(name):
    result = redis_conn.get(name)
    # Currently no way to change model type retrieved
    if result:
        return DecisionTree(json.loads(str(result, encoding='utf8')))
    else:
        return None


@app.route('/model/<name>/predict/')
def predict_with_model(name):
    row = request.get_json(force=True)
    model_func = retrieve_model(name)
    if model_func:
        return model_func(row)
    else:
        return make_response("No Such Model", 404)


if __name__ == '__main__':
    app.run()
