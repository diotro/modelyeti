from flask import Flask, request

from model import DecisionTree

app = Flask(__name__)

MODELS = {}

@app.route('/model/upload/decisiontree/<name>', methods=["POST"])
def upload_model(name):
    model = DecisionTree(request.get_json(force=True))
    print(request.get_json())
    print(MODELS)
    MODELS[name] = model
    return "OK"


@app.route('/model/<name>/predict/')
def predict_with_model(name):
    row = request.get_json(force=True)
    model_func = get_model_func(name)
    return model_func(row)


def get_model_func(name):
    return MODELS[name]


if __name__ == '__main__':
    app.run()
