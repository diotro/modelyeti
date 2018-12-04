import hashlib
import json
import subprocess
import tempfile

from yetiserver.app_factory import create_app

local_redis_port = 15321


def spin_up_app():
    """:return: an instance of the app created with the default test configuration"""
    _start_redis()
    app = _get_app()
    return app


def kill_app():
    _stop_redis()


def _get_app():
    with tempfile.NamedTemporaryFile('w', delete=False) as file:
        file.write(json.dumps({
            "redis": {
                "host": "localhost",
                "port": local_redis_port,
                "password": ""
            }
        }))
    return create_app(file.name)


def _start_redis():
    subprocess.run(['redis-server', '--port', str(local_redis_port), '--daemonize', 'yes'])


def _stop_redis():
    subprocess.run(['redis-cli', '-p', str(local_redis_port), 'FLUSHDB'])
    subprocess.run(['redis-cli', '-p', str(local_redis_port), 'shutdown'])


def hash_password(password):
    return hashlib.sha3_512(password.encode("utf8")).hexdigest()
