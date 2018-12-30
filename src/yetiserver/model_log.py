import redis

from yetiserver import redis_keys

def model_log_from_redis_conn(redis_conn):
    return ModelLogDao(redis_conn)

class ModelLogDao:
    def __init__(self, redis_conn: redis.Redis):
        self.rconn = redis_conn

    def retrieve_predictions_counter(self, user_name, model_name):
        response = self.rconn.get(redis_keys.for_prediction_count(user_name, model_name))
        if response is None:
            return 0
        else:
            return int(response.decode("utf8"))

    def increment_predictions_counter(self, user_name, model_name):
        self.rconn.incr(redis_keys.for_prediction_count(user_name, model_name))

