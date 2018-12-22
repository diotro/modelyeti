import subprocess
import redis


local_redis_port = 15321


def get_redis():
    class RedisContextManager:
        def __enter__(self):
            _start_redis()
            return redis.Redis(port=local_redis_port)

        def __exit__(self, exc_type, exc_val, exc_tb):
            _stop_redis()
    return RedisContextManager()

def kill_app():
    _stop_redis()


def _start_redis():
    subprocess.run(['redis-server', '--port', str(local_redis_port), '--daemonize', 'yes'])


def wipe_databases():
    subprocess.run(['redis-cli', '-p', str(local_redis_port), 'FLUSHDB'])


def _stop_redis():
    wipe_databases()
    subprocess.run(['redis-cli', '-p', str(local_redis_port), 'shutdown'])

