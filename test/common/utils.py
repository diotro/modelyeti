import hashlib


def hash_password(password: object) -> object:
    return hashlib.sha3_512(password.encode("utf8")).hexdigest()