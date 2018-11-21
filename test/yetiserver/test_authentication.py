from unittest import mock

import pytest

import yetiserver.authentication as auth
import hashlib


def test_register_user():
    mock_dao = mock.Mock()
    user_name = "user"
    email = "user@example.com"
    pass_hash = hashlib.sha512(b"password").hexdigest()

    auth.register_user(mock_dao, user_name, email, pass_hash)
    mock_dao.register_user.assert_called_once_with(user_name, email, pass_hash)


def test_register_user_invalid_user_name():
    mock_dao = mock.Mock()
    username = "   "
    email = "user@example.com"
    pass_hash = hashlib.sha3_512(b"password").hexdigest()

    with pytest.raises(ValueError):
        auth.register_user(mock_dao, username, email, pass_hash)
    mock_dao.register_user.assert_not_called()


@pytest.mark.parametrize("username", ["words", "username1", "jzucker", "WithCaps", "With_!@", "With$#^*@&#"])
def test_user_name_is_legal_true_cases(username):
    assert auth._user_name_is_legal(username)


@pytest.mark.parametrize("username", ["invalid username because of spaces", "", "a[]", "/a/", "/", ".", "../"])
def test_user_name_is_legal_false_cases(username):
    assert not auth._user_name_is_legal(username)


def test_register_user_but_another_user_exists():
    mock_dao = mock.Mock()
    user_name = "username"
    email = "user@example.com"
    pass_hash1 = hashlib.sha3_512(b"password").hexdigest()
    pass_hash2 = hashlib.sha3_512(b"p4ssword").hexdigest()

    auth.register_user(mock_dao, user_name, email, pass_hash1)
    with pytest.raises(auth.RegistrationError):
        mock_dao.register_user.side_effect = ValueError()
        auth.register_user(mock_dao, user_name, email, pass_hash2)
    assert mock_dao.register_user.call_count == 2
    assert mock_dao.called_with(user_name, email, pass_hash1)
    assert mock_dao.called_with(user_name, email, pass_hash2)


def test_check_credentials():
    username = "user"
    passhash = hashlib.sha3_512(b"password").hexdigest()
    mock_dao = mock.Mock()
    auth.check_credentials(mock_dao, username, passhash)

    assert mock_dao.called_once_with(username, passhash)

def test_check_credentials_with_invalid_password():
    username = "user"
    passhash = "not a real pass hash!"
    mock_dao = mock.Mock()
    with pytest.raises(ValueError):
        auth.check_credentials(mock_dao, username, passhash)