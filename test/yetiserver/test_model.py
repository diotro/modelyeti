import json

from yetiserver import model
from test.example_models import \
    all_test_decision_trees, \
    all_test_random_forests, \
    credit_score_decision_tree, \
    credit_score_random_forest


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
