from flask import Flask, request, make_response

from model import DecisionTree

app = Flask(__name__)

MODELS = {}

@app.route('/model/upload/decisiontree/<name>', methods=["POST"])
def upload_model(name):
    """Uploads a decision tree model with the given name"""
    model = DecisionTree(request.get_json(force=True))
    MODELS[name] = model
    return "OK"


@app.route('/model/<name>/predict/')
def predict_with_model(name):
    row = request.get_json(force=True)
    model_func = get_model_func(name)
    if model_func:
        return model_func(row)
    else:
        return make_response("No Such Model", 404)


def get_model_func(name):
    return MODELS[name]


if __name__ == '__main__':
    app.run()
