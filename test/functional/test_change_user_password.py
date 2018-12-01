import tempfile
import json
import hashlib

from yetiserver.app_factory import create_app

import subprocess

local_redis_port = 15321


def start_redis():
    subprocess.run(['redis-server', '--port', str(local_redis_port), '--daemonize', 'yes'])


def stop_redis():
    subprocess.run(['redis-cli', '-p', str(local_redis_port), 'FLUSHDB'])
    subprocess.run(['redis-cli', '-p', str(local_redis_port), 'shutdown'])


def get_app():
    with tempfile.NamedTemporaryFile('w', delete=False) as file:
        file.write(json.dumps({
            "redis": {
                "host": "localhost",
                "port": local_redis_port,
                "password": ""
            }
        }))
    return create_app(file.name)


start_redis()
app = get_app()
client = app.test_client()

username = "testuser"
passhash = hashlib.sha3_512(b"password").hexdigest()
passhash2 = hashlib.sha3_512(b"p4$sword").hexdigest()


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
    stop_redis()
