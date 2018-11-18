import json

from yetiserver import model


def create_decision_tree_json(income_split, left_credit_score_split, right_credit_score_split):
    return {
        "split_col": "income",
        "split_val": income_split,
        "left": {
            "split_col": "credit_score",
            "split_val": left_credit_score_split,
            "left": "decline",
            "right": "accept"
        },
        "right": {
            "split_col": "credit_score",
            "split_val": right_credit_score_split,
            "left": "decline",
            "right": "accept"
        }
    }


credit_score_decision_tree = model.DecisionTree({
    "model_type": "decision_tree",
    "model": create_decision_tree_json(75_000, 700, 500)
})

credit_score_random_forest = model.RandomForest({
    "model_type": "random_forest",
    "model": [create_decision_tree_json(75_000, 700, 500),
              create_decision_tree_json(70_000, 675, 300),
              create_decision_tree_json(80_000, 680, 500)]
})

all_test_decision_trees = [credit_score_decision_tree]
all_test_random_forests = [credit_score_random_forest]
