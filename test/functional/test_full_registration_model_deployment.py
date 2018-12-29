from test.functional.test_register_user_flow import register_user
from test.functional.fixtures import hash_password, get_test_app
from test.example_models import credit_score_decision_tree_json


def test_registration_model_deployment():
    username = "testuser"
    passhash = hash_password("password")
    model_name = "csdt"

    with get_test_app() as app:
        client = app.test_client()

        def upload_model(username, passhash, model, model_name):
            client.post(f"/v1/model_management/upload/{username}/{model_name}/",
                        json=model,
                        headers={"password_hash_sha3_512": passhash})

        def make_prediction(username, passhash, model_name, input_data):
            return client.get(f"/v1/model_management/{username}/{model_name}/predict/",
                              json=input_data,
                              headers={"password_hash_sha3_512": passhash})

        register_user(client, username, passhash, "email@example.com")
        upload_model(username, passhash, credit_score_decision_tree_json, model_name)
        response = make_prediction(username, passhash, model_name, {"income": 10, "credit score": 10})

        assert response.status == "200 OK"
        assert b"decline" in response.data
