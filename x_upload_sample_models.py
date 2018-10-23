import json
import requests


def upload_model(name, m):
    requests.post(f"http://localhost:5000/model/upload/decisiontree/{name}", data=json.dumps(m))


if __name__ == '__main__':
    upload_model("credit", {
        "split_col": "income",
        "split_val": 75_000,
        "left": {
            "split_col": "credit_score",
            "split_val": 700,
            "left": "decline",
            "right": "accept"
        },
        "right": {
            "split_col": "credit_score",
            "split_val": 500,
            "left": "decline",
            "right": "accept"
        }
    })
