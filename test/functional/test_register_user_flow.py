from test.functional.fixtures import get_test_app, hash_password


with get_test_app() as app:
    client = app.test_client()

    username = "testuser"
    passhash = hash_password("passwordasdfa")


    def register_user(username, passhash, email):
        client.post("/user/register/", json={
            "username": username,
            "passhash": passhash,
            "user_email": email
        })

    register_user("testuser", passhash, "user@example.com")
    assert app.auth.check_credentials(username, passhash)
