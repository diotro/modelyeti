from src import yetiserver as dao

from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/model/upload/<user_name>/<model_name>', methods=["POST"])
def upload_model(user_name, model_name):
    """Uploads a decision tree model with the given name"""
    # TODO authenticate
    dao.store_model(user_name, model_name, request.get_json(force=True))
    return "OK"


@app.route('/model/<user_name>/<model_name>/predict/')
def predict_with_model(user_name, model_name):
    # TODO authenticate
    row = request.get_json(force=True)
    model_func = dao.retrieve_model(user_name, model_name)
    if model_func:
        return model_func(row)
    else:
        return make_response("No Such Model", 404)


if __name__ == '__main__':
    app.run()
