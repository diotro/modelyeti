import hashlib

from test.functional.fixtures import spin_up_app, kill_app, hash_password

app = spin_up_app()
client = app.test_client()

username = "testuser"
passhash = hash_password("passwordasdfa")

client.post("/user/register/", json={
    "username": "testuser",
    "passhash": passhash,
    "user_email": "user@example.com"
})

try:
    assert app.auth.check_credentials(username, passhash)
finally:
    kill_app()