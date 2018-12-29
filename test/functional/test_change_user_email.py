import json

from test.common.utils import hash_password
from test.functional.fixtures import get_test_app
from test.functional.test_register_user_flow import register_user


def change_user_email(client, username, passhash, new_email):
    client.post("/v1/user_management/user/update_email/", json={
        "username": username,
        "passhash": passhash,
        "new_email": new_email
    })


def get_user_info(client, username, passhash):
    response = client.get("/v1/user_management/user/info/", json={
        "username": username,
        "passhash": passhash
    })
    return response.json


def test_change_user_password():
    username = "testuser"
    passhash = hash_password("password")
    email1 = "email1@example.com"
    email2 = "email2@example.com"

    with get_test_app() as app:
        with app.test_client() as client:
            register_user(client, username, passhash, email1)
            assert get_user_info(client, username, passhash)["email"] == email1

            change_user_email(client, username, passhash, email2)
            assert get_user_info(client, username, passhash)["email"] == email2
