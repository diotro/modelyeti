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

client.post("/user/register/", json={
    "username": "testuser",
    "passhash": passhash,
    "user_email": "user@example.com"
})

try:
    assert app.auth.check_credentials(username, passhash)
finally:
    stop_redis()
