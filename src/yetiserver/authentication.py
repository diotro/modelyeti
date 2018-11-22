import re

import redis

from yetiserver.logger import logging


def register_user(dao, user_name, user_email, hashed_password):
    """Registers a user with the given username, email, and bcrypt-hashed password.
    :return: True if the user is created, false if they were nto
    :raises ValueError: if the given user_name is invalid
    :raises RegistrationError: if there was an error in registering the user.
    """
    logging.debug(f"Account {user_name} registered with email {user_email} and password hash {hashed_password}")

    if not _user_name_is_legal(user_name):
        raise ValueError(f"Illegal username '{user_name}'")

    # TODO send an email to verify email address
    try:
        return dao.register_user(user_name, user_email, hashed_password)
    except ValueError or redis.RedisError as e:
        raise RegistrationError("Could not register user.", e)


class RegistrationError(Exception):
    pass


def _user_name_is_legal(user_name):
    return re.compile('[A-Za-z0-9_!@#$%^&*]+').fullmatch(user_name)


def check_credentials(dao, user_name, hashed_password):
    """Checks the given credentials to see if the user and password match.

    :param dao: the DAO to use
    :param user_name: the name of the user to check
    :param hashed_password: the hashed password the user is trying to use to login
    :return: whether the user has provided credentials they can use to login
    """
    if not re.compile("[0-9a-f]{128}").fullmatch(hashed_password):
        raise ValueError("hashed password must be a hex digest of a sha3_512 hash")
    return dao.check_credentials(user_name, hashed_password)
