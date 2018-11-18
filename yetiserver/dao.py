import json
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
import redis

from yetiserver import model

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


def _get_redis_connection(redis_class=None):
    """ Using the globals `__host`, `__port`, and `__password`, returns a redis connection
    to the redis server specified.

    :param redis_class: the class to use when creating the redis connection. Defaults to `redis.Redis`
    if none is provided
    :return: A `redis.Redis` connected to the database.
    :raises redis.RedisException: if can't connect to the database
    """
    redis_class = redis_class or redis.Redis
    # global __redis_conn
    # if not __redis_conn:
    #     __redis_conn = redis_class(host=__host, port=__port, password=__password)
    # return __redis_conn
    return redis_class(host=__host, port=__port, password=__password)


def retrieve_model(user_name, model_name, rconn=None):
    """Retrieves a model from the database.

    :param user_name: the name of the user who owns the model
    :param model_name: the name of the model to retrieve
    :param rconn: the redis connection to use, or None if should use the default
    :return: The model, or None if there is no such model.
    """
    rconn = rconn or _get_redis_connection()
    serialized_model = retrieve_serialized_model(rconn, user_name, model_name)
    try:
        return model.deserialize(serialized_model)
    except ValueError:
        return None


def retrieve_serialized_model(rconn, user_name, model_name):
    """Retrieves the serialized model from the database.

    :param rconn: the database to retrieve the model from
    :param user_name: the user who owns the model to retrieve
    :param model_name: the model to retrieve
    :return:
    """
    return rconn.get(__key_for_model(user_name, model_name))


def __key_for_model(user_name, model_name):
    """What key should the model of the given name belonging to the user with the given name be
    stored under?

    :return: The key that the model is stored under.
    """
    return f"models::${user_name}::${model_name}"


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
        rconn.set(__key_for_model(user_name, model_name), model.serialize(model_to_store))
        return True
    except redis.RedisError as e:
        logging.error(e)
        return False
