import json
from yetiserver.logger import logging
from collections import Counter


def deserialize(model_string):
    model_classes = {
        "decision_tree": DecisionTree,
        "random_forest": RandomForest
    }

    logging.debug(f"attempting to deserialize model {model_string}")
    try:
        model_json = json.loads(model_string)
        model_type = model_json["model_type"]
        model_class = model_classes[model_type]
        return model_class(model_json)
    except TypeError or AttributeError or KeyError or ValueError as e:
        logging.error(e)
        return None


def serialize(model):
    logging.debug(f"attempting to serialize model {model}")
    try:
        return json.dumps(model.data)
    except AttributeError or ValueError or TypeError:
        logging.debug("could not serialize model {model}")
        return None


class DecisionTree:
    """A simple decision tree. Currently supports only numerical values and pure categorical outputs."""

    def __init__(self, data):
        """Creates a decision tree.

        :param data: the JSON data that was used to construct the decision tree
        """
        self.data = data
        self.model_func = DecisionTree._deserialize_decision_tree_from_json(data["model"])

    def __call__(self, *args, **kwargs):
        return self.model_func(*args, **kwargs)

    def get_original_json(self):
        return self.data

    @staticmethod
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
            # TODO add support for continuous prediction variable, error bar, in general more types
            # of terminal nodes based on what is supported in common ML libraries
            return lambda x: data

        # Dictionary case: extract all the data, create models of left and right, dispatch to left or right
        # model based on comparison of split_col.
        try:
            split_column = data["split_col"]
            split_value = data["split_val"]

            left_model = DecisionTree._deserialize_decision_tree_from_json(data["left"])
            right_model = DecisionTree._deserialize_decision_tree_from_json(data["right"])

        except KeyError or ValueError as e:
            raise ValueError(f"Invalid JSON {json.dumps(data)} for Decision Tree.", e)

        def model_func(row):
            return left_model(row) if row[split_column] < split_value else right_model(row)

        return model_func


class RandomForest:
    """A random forest. Essentially just a list of `DecisionTree`s."""

    def __init__(self, data):
        """Data is expected to be a list of dictionaries, each parseable as a DecisionTree"""
        self.data = data
        self.func = RandomForest._read_func_from_data(data["model"])

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def get_original_json(self):
        return self.data

    @staticmethod
    def _read_func_from_data(data):
        trees = [DecisionTree._deserialize_decision_tree_from_json(item) for item in data]

        def predict(input):
            # TODO this only works for categorical outputs, have to update for continuous output
            predictions = [tree(input) for tree in trees]
            logging.log(logging.DEBUG, predictions)
            # Returns as array of length one, containing tuple of item and count, so value is at index [0][0]
            most_common = Counter(predictions).most_common(1)
            logging.log(logging.DEBUG, most_common)
            return most_common[0][0]

        return predict
