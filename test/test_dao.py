import pytest
from test.example_models import credit_score_decision_tree, credit_score_random_forest
import redis

from yetiserver import dao


@pytest.mark.requires_local_redis
def test_can_connect_to_local_redis():
    conn = dao._get_redis_connection()
    assert conn


def test_raise_exception_on_failure_to_connect_to_db():
    class RedisExceptionThrower:
        def __init__(self, *args, **kwargs):
            raise redis.RedisError

    with pytest.raises(redis.RedisError):
        dao._get_redis_connection(redis_class=RedisExceptionThrower)


def test_setting_connection_parameters_changes_connection_details():
    class RedisRememberArgs:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    before_host, before_port, before_pass = dao.__host, dao.__port, dao.__password
    dao.set_redis_connection_parameters("host", "port", "pass")

    r = dao._get_redis_connection(redis_class=RedisRememberArgs)
    assert r.kwargs['host'] == "host"
    assert r.kwargs['port'] == "port"
    assert r.kwargs['password'] == "pass"

    dao.set_redis_connection_parameters(before_host, before_port, before_pass)


@pytest.mark.requires_local_redis
def test_can_store_retrieve_decision_tree():
    success = dao.store_model("user1", "model1", credit_score_decision_tree)
    assert success
    model = dao.retrieve_model("user1", "model1")
    assert credit_score_decision_tree.data == model.data


@pytest.mark.requires_local_redis
def test_can_store_retrieve_random_forest():
    success = dao.store_model("user1", "model1", credit_score_random_forest)
    assert success
    model = dao.retrieve_model("user1", "model1")
    assert credit_score_random_forest.data == model.data

@pytest.mark.requires_local_redis
def test_retrieved_model_same_as_original_model():
    dao.store_model("user2", "model2", credit_score_decision_tree)
    retrieved_model = dao.retrieve_model("user2", "model2")
    for (income, credit) in [(100, 100), (100_000, 100), (100_000, 1000), (100, 1000)]:
        data = {"income": income, "credit_score": credit}
        assert credit_score_decision_tree(data) == retrieved_model(data)


def test_attempt_to_retrieve_model_doesnt_exist_returns_none():
    assert dao.retrieve_model("nonexistent_user", "model1") == None
    assert dao.retrieve_model("user1", "no_such_model") == None


def test_attempt_to_store_invalid_model_returns_false():
    assert not dao.store_model("user1", "model1", "ahaha not a model")
