from test.functional.fixtures import spin_up_app, kill_app, hash_password

username = "testuser"
passhash = hash_password("password")
passhash2 = hash_password("p4$sword")

app = spin_up_app()
client = app.test_client()

try:
    client.post("/user/register/", json={
        "username": username,
        "passhash": passhash,
        "user_email": "user@example.com"
    })
    assert app.auth.check_credentials(username, passhash)
    assert not app.auth.check_credentials(username, passhash2)

    client.post("/user/change_password/", json={
        "username": username,
        "old_password": passhash,
        "new_password": passhash2
    })
    assert not app.auth.check_credentials(username, passhash)
    assert app.auth.check_credentials(username, passhash2)
finally:
    kill_app()
