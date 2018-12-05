from src.yetiserver import model


# Not pytest fixtures because they are static, immutable values. No need to create new one
# for each test.


def create_credit_decision_tree_json(income_split, left_credit_score_split, right_credit_score_split):
    return {
        "split_col": "income",
        "split_val": income_split,
        "left": {
            "split_col": "credit score",
            "split_val": left_credit_score_split,
            "left": "decline",
            "right": "approve"
        },
        "right": {
            "split_col": "credit score",
            "split_val": right_credit_score_split,
            "left": "decline",
            "right": "approve"
        }
    }


credit_score_decision_tree_json = {
    "model_type": "decision_tree",
    "model": create_credit_decision_tree_json(75_000, 700, 500)
}
credit_score_decision_tree = model.DecisionTree(credit_score_decision_tree_json)

credit_score_random_forest = model.RandomForest({
    "model_type": "random_forest",
    "model": [create_credit_decision_tree_json(75_000, 700, 500),
              create_credit_decision_tree_json(75_000, 675, 300),
              create_credit_decision_tree_json(75_000, 680, 550)]
})

all_test_decision_trees = [credit_score_decision_tree]
all_test_random_forests = [credit_score_random_forest]