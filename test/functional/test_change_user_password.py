from test.functional.test_register_user_flow import register_user
from test.functional.fixtures import get_test_app, wipe_databases, hash_password


def change_user_password(client, username, old_pass_hash, new_pass_hash):
    client.post("/user/change_password/", json={
        "username": username,
        "old_password": old_pass_hash,
        "new_password": new_pass_hash
    })


def test_change_user_password():
    username = "testuser"
    passhash = hash_password("password")
    passhash2 = hash_password("p4$sword")

    with get_test_app() as app:
        client = app.test_client()

        register_user(client, username, passhash, "any_old_email_will_do@example.com")

        assert app.auth.check_credentials(username, passhash)
        assert not app.auth.check_credentials(username, passhash2)

        change_user_password(client, username, passhash, passhash2)

        assert not app.auth.check_credentials(username, passhash)
        assert app.auth.check_credentials(username, passhash2)

        wipe_databases()