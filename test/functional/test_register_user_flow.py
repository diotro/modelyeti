from test.functional.fixtures import get_test_app, hash_password


def register_user(client, username, passhash, email):
    client.post("/v1/user_management/user/register/", json={
        "username": username,
        "passhash": passhash,
        "email": email
    })


def test_register_user():
    with get_test_app() as app:
        client = app.test_client()

        username = "testuser"
        passhash = hash_password("passwordasdfa")

        register_user(client, "testuser", passhash, "user@example.com")
        assert app.auth.check_credentials(username, passhash)
