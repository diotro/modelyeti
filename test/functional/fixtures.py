import hashlib

from test.common.local_redis_connection import _start_redis, kill_app, local_redis_port, wipe_databases
from yetiserver.app_factory import create_app
from test.common.utils import hash_password

def get_test_app():
    """Meant to be used in `with` blocks, as in:

    `with TestApp() as app:
            with app.test_client() as client:
                ...
    `
    """

    class TestApp:
        def __enter__(self):
            _start_redis()
            return _get_app()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return kill_app()

    return TestApp()


def _get_app():
    wipe_databases()
    return create_app({
            "redis": {
                "host": "localhost",
                "port": local_redis_port,
                "password": ""
            }
        })
