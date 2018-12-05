import hashlib
import json
import subprocess
import tempfile


from yetiserver.app_factory import create_app

local_redis_port = 15321


def get_test_app():
    class TestApp:
        def __enter__(self):
            _start_redis()
            return _get_app()
        def __exit__(self, exc_type, exc_val, exc_tb):
            return kill_app()
    return TestApp()

def _get_app():
    with tempfile.NamedTemporaryFile('w', delete=False) as file:
        file.write(json.dumps({
            "redis": {
                "host": "localhost",
                "port": local_redis_port,
                "password": ""
            }
        }))
    wipe_databases()
    return create_app(file.name)

def kill_app():
    _stop_redis()


def _start_redis():
    subprocess.run(['redis-server', '--port', str(local_redis_port), '--daemonize', 'yes'])


def wipe_databases():
    subprocess.run(['redis-cli', '-p', str(local_redis_port), 'FLUSHDB'])


def _stop_redis():
    wipe_databases()
    subprocess.run(['redis-cli', '-p', str(local_redis_port), 'shutdown'])


def hash_password(password):
    return hashlib.sha3_512(password.encode("utf8")).hexdigest()