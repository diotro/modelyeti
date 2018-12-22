import redis


def connect_to_database(config):
    """Creates a database connection using the credentials found in the file with the given name.

    :param config_filename: the name of the file to parse. Must be a json file, containing only one dictionary. That
    dictionary must have a key "redis", which leads to a dictionary containing "host", "port", and "password".
    :return: a :py:class:`redis.Redis` connection
    """
    try:
        redis_config = config["redis"]
        host = redis_config["host"]
        port = redis_config["port"]
        password = redis_config["password"]
        return redis.Redis(host, port, password)
    except redis.RedisError as e:
        raise e