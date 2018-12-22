from unittest import mock

import pytest

from yetiserver import authentication, redis_keys
from yetiserver.authentication import UserManager, UserDao, UserNotFoundError
import hashlib


def test_register_user():
    mock_dao = mock.Mock()
    auth = UserManager(mock_dao)
    user_name = "user"
    email = "user@example.com"
    pass_hash = hashlib.sha512(b"password").hexdigest()

    auth.register_user(user_name, email, pass_hash)
    mock_dao.add_user.assert_called_once_with(user_name, email, pass_hash)


def test_register_user_invalid_user_name():
    mock_dao = mock.Mock()
    auth = UserManager(mock_dao)
    username = "   "
    email = "user@example.com"
    pass_hash = hashlib.sha3_512(b"password").hexdigest()

    with pytest.raises(ValueError):
        auth.register_user(username, email, pass_hash)
    mock_dao.register_user.assert_not_called()


@pytest.mark.parametrize("username", ["words", "username1", "jzucker", "WithCaps", "With_!@", "With$#^*@&#"])
def test_user_name_is_legal_true_cases(username):
    assert authentication._user_name_is_legal(username)


@pytest.mark.parametrize("username", ["invalid username because of spaces", "", "a[]", "/a/", "/", ".", "../"])
def test_user_name_is_legal_false_cases(username):
    assert not authentication._user_name_is_legal(username)


def test_register_user_but_another_user_exists():
    mock_dao = mock.Mock()
    auth = UserManager(mock_dao)
    user_name = "username"
    email = "user@example.com"
    pass_hash1 = hashlib.sha3_512(b"password").hexdigest()
    pass_hash2 = hashlib.sha3_512(b"p4ssword").hexdigest()

    auth.register_user(user_name, email, pass_hash1)
    with pytest.raises(authentication.RegistrationError):
        mock_dao.add_user.side_effect = ValueError()
        auth.register_user(user_name, email, pass_hash2)
    assert mock_dao.add_user.call_count == 2
    assert mock_dao.add_user.called_with(user_name, email, pass_hash1)
    assert mock_dao.add_user.called_with(user_name, email, pass_hash2)


def test_check_credentials():
    mock_dao = mock.Mock()
    auth = UserManager(mock_dao)
    username = "user"
    passhash = hashlib.sha3_512(b"password").hexdigest()
    mock_dao.retrieve_password_hash_for_user.return_value(passhash)
    auth.check_credentials(username, passhash)

    assert mock_dao.called_once_with(username, passhash)


def test_check_credentials_with_invalid_password():
    mock_dao = mock.Mock()
    auth = UserManager(mock_dao)
    username = "user"
    passhash = "not a real pass hash!"
    with pytest.raises(ValueError):
        auth.check_credentials(username, passhash)


def test_update_password():
    mock_dao = mock.Mock()
    auth = UserManager(mock_dao)
    username = "user"
    passhash = hashlib.sha3_512(b"password").hexdigest()
    auth.update_password(username, passhash)
    assert mock_dao.update_password_hash_for_user.called_with(username, passhash)


def test_delete_user():
    mock_dao = mock.Mock()
    auth = UserManager(mock_dao)
    username = "user"
    auth.delete_user(username)
    assert mock_dao.delete_user.called_once_with(username)


def test_retrieve_password_hash_for_user():
    mock_rconn = mock.Mock()
    dao = UserDao(mock_rconn)
    dao.user_exists = mock.Mock(return_value=True)
    username = "user"
    dao.retrieve_password_hash_for_user(username)
    mock_rconn.get.assert_called_once_with(redis_keys.for_user_password_hash(username))


def test_retrieve_password_hash_for_user_that_does_not_exist():
    mock_rconn = mock.Mock()
    dao = UserDao(mock_rconn)
    dao.user_exists = mock.Mock(return_value=False)
    username = "user"
    with pytest.raises(UserNotFoundError):
        dao.retrieve_password_hash_for_user(username)


def test_update_password_has_for_user():
    mock_rconn = mock.Mock()
    dao = UserDao(mock_rconn)
    dao.user_exists = mock.Mock(return_value=True)
    username = "user"
    passhash = hashlib.sha3_512(b"password").hexdigest()
    dao.update_password_hash_for_user(username, passhash)
    assert mock_rconn.set.called_once_with(redis_keys.for_user_password_hash(username), "asdf")


def test_update_password_has_for_user_that_does_not_exist():
    mock_rconn = mock.Mock()
    dao = UserDao(mock_rconn)
    dao.user_exists = mock.Mock(return_value=False)
    username = "user"
    passhash = hashlib.sha3_512(b"password").hexdigest()
    with pytest.raises(UserNotFoundError):
        dao.update_password_hash_for_user(username, passhash)


def test_remove_user_calls_delete():
    mock_rconn = mock.Mock()

    dao = UserDao(mock_rconn)
    dao.delete_user("user1")

    mock_rconn.delete.assert_called_with(redis_keys.for_user_information("user1"))