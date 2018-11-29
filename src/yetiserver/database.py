import json

import redis


def database_connection_from_file(config_filename):
    """Creates a database connection using the credentials found in the file with the given name.

    :param config_filename: the name of the file to parse. Must be a
    :return: a :py:class:`redis.Redis` connection
    """
    with open(config_filename, 'r') as config_file:
        config = json.load(config_file)

    try:
        host = config["redis_host"]
        port = config["redis_port"]
        password = config["redis_password"]
    except KeyError as e:
        raise e
    else:
        try:
            return redis.Redis(host, port, password)
        except redis.RedisError as e:
            raise e
