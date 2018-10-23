import json


class DecisionTree:
    """A simple decision tree. Currently supports only numerical values and pure categorical outputs."""

    def __init__(self, data):
        """Creates a decision tree.

        :param data: the JSON data that was used to construct the decision tree
        """
        self.data = data
        self.model_func = _deserialize_decision_tree_from_json(data)

    def __call__(self, *args, **kwargs):
        return self.model_func(*args, **kwargs)


def _deserialize_decision_tree_from_json(data):
    """Deserializes the model from the given JSON. The JSON must have the following form:

    A DT is one of:
    - String, the result to return for this node.
    - {"split_col": String, "split_val": String, "left": DT, "right": DT}, specifying a column to split on,
       the value to split on (if the input is lower than that value, goes to the left, greater to the right)
       and the left/right node of the tree.

    :param data: JSON in the above-described DT format.
    :rtype: Dict -> String
    :return: the function that makes predictions for the type of data the model was produced for
    """
    # String case is simple: always return the string at the terminal node
    if isinstance(data, str):
        return lambda x: data

    # Dictionary case: extract all the data, create models of left and right, dispatch to left or right
    # model based on comparison of split_col.
    try:
        split_column = data["split_col"]
        split_value = data["split_val"]

        left_model = DecisionTree(data["left"])
        right_model = DecisionTree(data["right"])

    except KeyError or ValueError as e:
        raise ValueError(f"Invalid JSON {json.dumps(data)} for Decision Tree construction.", e)

    def model_func(row):
        return left_model(row) if row[split_column] < split_value else right_model(row)

    return model_func


