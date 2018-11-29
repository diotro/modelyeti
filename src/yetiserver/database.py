import json

import redis


def database_connection_from_file(config_filename):
    """Creates a database connection using the credentials found in the file with the given name.

    :param config_filename: the name of the file to parse. Must be a json file, containing only one dictionary. That
    dictionary must have a key "redis", which leads to a dictionary containing "host", "port", and "password".
    :return: a :py:class:`redis.Redis` connection
    """
    with open(config_filename, 'r') as config_file:
        redis_config = json.load(config_file)["redis"]

    try:
        host = redis_config["host"]
        port = redis_config["port"]
        password = redis_config["password"]
    except KeyError as e:
        raise e
    else:
        try:
            return redis.Redis(host, port, password)
        except redis.RedisError as e:
            raise e
