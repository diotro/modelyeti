import redis
import json
import unittest.mock as mock

from yetiserver import model, redis_keys
from test.example_models import \
    all_test_decision_trees, \
    all_test_random_forests, \
    credit_score_decision_tree, \
    credit_score_random_forest

def model_manager_mocked():
    """Mocks the DAO for a manager."""
    mock_dao = mock.Mock(model.ModelDao)
    return model.ModelManager(mock_dao), mock_dao


def test_attempt_to_retrieve_model_doesnt_exist_returns_none():
    manager, dao = model_manager_mocked()
    dao.retrieve_serialized_model.return_value = None
    assert manager.retrieve_model("nonexistent_user", "model1") is None
    assert manager.retrieve_model("user1", "no_such_model") is None


def test_attempt_to_store_invalid_model_returns_false():
    manager, dao = model_manager_mocked()
    dao.store_serialized_model.return_value = False
    assert not manager.store_model("user1", "model1", "ahaha not a model")


def model_manager_connection_mocked():
    """Mocks the redis connection for a manager and DAO."""
    redis_mock = mock.Mock(redis.Redis)
    dao = model.ModelDao(redis_mock)
    manager = model.ModelManager(dao)
    return (manager, dao, redis_mock)


def test_storing_model_in_correct_place():
    manager, dao, rconn_mock = model_manager_connection_mocked()
    user = "user1"
    model_name = "model1"
    manager.store_model(user, model_name, credit_score_decision_tree)

    expected_key = redis_keys.for_model(user, model_name)
    expected_value = model.serialize(credit_score_decision_tree)
    rconn_mock.set.assert_called_once_with(expected_key, expected_value)


def test_retrieving_model_looks_in_correct_place():
    manager, dao, rconn_mock = model_manager_connection_mocked()

    user = "user1"
    model_name = "model1"
    dao.retrieve_serialized_model(user, model_name)

    expected_key = redis_keys.for_model(user, model_name)
    rconn_mock.get.assert_called_once_with(expected_key)


def de_and_re_serialize(a_model):
    return json.loads(model.serialize(model.deserialize(json.dumps(a_model.get_original_json()))))


def test_serialize_inverse_deserialize_decision_tree():
    for tree in all_test_decision_trees:
        assert tree.get_original_json() == de_and_re_serialize(tree)


def test_serialize_inverse_deserialize_random_forest():
    for forest in all_test_random_forests:
        assert forest.get_original_json() == de_and_re_serialize(forest)


def test_decision_tree():
    tree = credit_score_decision_tree
    assert tree({"income": 100000, "credit score": 1000}) == "approve"
    assert tree({"income": 10000, "credit score": 1000}) == "approve"
    assert tree({"income": 10000, "credit score": 100}) == "decline"
    assert tree({"income": 10000, "credit score": 900}) == "approve"


def test_random_forest():
    tree = credit_score_random_forest
    assert tree({"income": 100000, "credit score": 1000}) == "approve"
    assert tree({"income": 10000, "credit score": 1000}) == "approve"
    assert tree({"income": 10000, "credit score": 100}) == "decline"
    assert tree({"income": 10000, "credit score": 900}) == "approve"

    assert tree({"income": 80000, "credit score": 520}) == "approve"
    assert tree({"income": 80000, "credit score": 560}) == "approve"
    assert tree({"income": 80000, "credit score": 499}) == "decline"
    assert tree({"income": 10000, "credit score": 900}) == "approve"
