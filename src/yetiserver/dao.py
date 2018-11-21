import redis

from yetiserver import redis_keys, model
from yetiserver.logger import logging

__host = 'localhost'
__port = 6379
__password = ''
__redis_conn = None


def set_redis_connection_parameters(host, port, password):
    """Sets the host, port, and password used to connect to redis."""
    global __host, __port, __password
    __host = host
    __port = port
    __password = password


def _get_redis_connection():
    """ Using the globals `__host`, `__port`, and `__password`, returns a redis connection
    to the redis server specified.
    :return: A `redis.Redis` connected to the database.
    :raises redis.RedisException: if can't connect to the database
    """
    global __redis_conn
    # Only update connection if there is no defined connection, or the class requested is different
    if not __redis_conn:
        __redis_conn = redis.Redis(host=__host, port=__port, password=__password)
    return __redis_conn


def retrieve_model(user_name, model_name, rconn=None):
    """Retrieves a model from the database.

    :param user_name: the name of the user who owns the model
    :param model_name: the name of the model to retrieve
    :param rconn: the redis connection to use, or None if should use the default
    :return: The model, or None if there is no such model.
    """
    rconn = rconn or _get_redis_connection()
    serialized_model = retrieve_serialized_model(user_name, model_name, rconn)
    if serialized_model is None:
        return None
    return model.deserialize(serialized_model)


def retrieve_serialized_model(user_name, model_name, rconn=None):
    """Retrieves the serialized model from the database.

    :param rconn: the database to retrieve the model from
    :param user_name: the user who owns the model to retrieve
    :param model_name: the model to retrieve
    :return: JSON, parseable as a model, if the given user has a model with the given name. Returns None if there is
    no model with the given name
    :raise ValueError: if the model isn't deserializable
    :raise redis.redisError: if there is an issue connecting to the database
    """
    rconn = rconn or _get_redis_connection()
    try:
        return rconn.get(redis_keys.for_model(user_name, model_name))
    except redis.RedisError as e:
        logging.error(e)
        return None


def store_model(user_name, model_name, model_to_store, rconn=None):
    """Stores the given model in redis.

    :param user_name: the name of the user who is storing the model
    :param model_name: the name of the model to store
    :param model_to_store:
    :param rconn: a redis connection, if one other than the default should be used
    :return: a truthy value if storing the model succeeded, falsey if not
    """
    try:
        rconn = rconn or _get_redis_connection()
        rconn.set(redis_keys.for_model(user_name, model_name), model.serialize(model_to_store))
        return True
    except redis.RedisError as e:
        logging.error(e)
        return False


def check_credentials(user_name, hashed_password, rconn=None):
    """Checks the credentials to see if the user should be allowed to use the model.

    :param user_name: The name of the user to check
    :param hashed_password: the hashed password the user has provided
    :param rconn: the connection to redis
    :return: True if the username exists in the database and has the same hashed password as provided, false
    if either the username doesn't exist or the password hash provided is different than in the database.
    :raise redis.RedisError: if redis has an error during this operation
    """
    try:
        rconn = rconn or _get_redis_connection()
        retrieved_pass_hash = rconn.get(redis_keys.for_user_password_hash(user_name))
        return retrieved_pass_hash is not None and retrieved_pass_hash == hashed_password
    except redis.RedisError as e:
        logging.error(e)
        raise e


def register_user(user_name, user_email, hashed_password, rconn=None):
    try:
        rconn = rconn or _get_redis_connection()
        if rconn.sismember(redis_keys.for_user_set(), user_name):
            logging.info(f"Attempted signup for taken username: {user_name}")
            raise ValueError("username is taken")
        rconn.pipeline() \
            .set(redis_keys.for_user_password_hash(user_name), hashed_password) \
            .set(redis_keys.for_user_email(user_name), user_email) \
            .execute()

    except redis.RedisError as e:
        logging.error(e)
        raise e
