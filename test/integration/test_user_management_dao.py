import pytest

from yetiserver import redis_keys
from yetiserver.authentication import UserDao, UserNotFoundError
from test.common import local_redis_connection
from test.common.utils import hash_password

user = "username"
email = "email@example.com"
passhash = hash_password("p@ssword")


@pytest.fixture
def dao():
    with local_redis_connection.get_redis() as rconn:
        yield UserDao(rconn)


def test_add_user(dao):
    dao.add_user(user, email, passhash)

    rconn = dao.rconn
    assert email.encode('utf8') == rconn.get(redis_keys.for_user_email(user))
    assert passhash.encode('utf8') == rconn.get(redis_keys.for_user_password_hash(user))
    assert rconn.sismember(redis_keys.for_user_set(), user)


def test_retrieve_password_hash_for_user(dao):
    rconn = dao.rconn
    with pytest.raises(UserNotFoundError):
        dao.retrieve_password_hash_for_user(user)

    rconn.sadd(redis_keys.for_user_set(), user)
    rconn.set(redis_keys.for_user_password_hash(user), passhash.encode("utf8"))
    assert passhash.encode('utf8') == dao.retrieve_password_hash_for_user(user)


def test_update_user_email(dao):
    rconn = dao.rconn
    new_email = "email2@example.com"
    with pytest.raises(UserNotFoundError):
        dao.update_user_email(user, new_email)

    rconn.sadd(redis_keys.for_user_set(), user)
    dao.update_user_email(user, new_email)
    assert new_email.encode('utf8') == rconn.get(redis_keys.for_user_email(user))

def test_get_user_info(dao):

    assert dao.user_info(user) is None

    dao.add_user(user, email, passhash)

    assert dao.user_info(user) is not None
    assert dao.user_info(user) == {
        "username": user,
        "email": email
    }
