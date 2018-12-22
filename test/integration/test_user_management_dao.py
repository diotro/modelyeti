import pytest

from yetiserver import redis_keys
from yetiserver.authentication import UserDao, UserNotFoundError
from test.common import local_redis_connection
from test.common.utils import hash_password

user = "username"
email = "email@example.com"
hpass = hash_password("p@ssword")


@pytest.fixture
def dao():
    with local_redis_connection.get_redis() as rconn:
        yield UserDao(rconn)


def test_add_user(dao):
    dao.add_user(user, email, hpass)

    rconn = dao.rconn
    assert email.encode('utf8') == rconn.get(redis_keys.for_user_email(user))
    assert hpass.encode('utf8') == rconn.get(redis_keys.for_user_password_hash(user))
    assert rconn.sismember(redis_keys.for_user_set(), user)


def test_retrieve_password_hash_for_user(dao):
    rconn = dao.rconn
    with pytest.raises(UserNotFoundError):
        dao.retrieve_password_hash_for_user(user)

    dao.add_user(user, email, hpass)
    assert hpass.encode('utf8') == dao.retrieve_password_hash_for_user(user)