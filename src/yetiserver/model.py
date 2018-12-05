import json
import traceback

import redis
from collections import Counter

from yetiserver import redis_keys


def model_manager_from_redis_conn(rconn):
    return ModelManager.from_db_connection(rconn)


class ModelManager:
    """Provides tools to store and retrieve models."""

    def __init__(self, dao):
        self.dao = dao

    @staticmethod
    def from_db_connection(db_conn):
        return ModelManager(ModelDao(db_conn))

    def retrieve_model(self, user_name, model_name):
        """Retrieves a model from the database.

        :param user_name: the name of the user who owns the model
        :param model_name: the name of the model to retrieve
        :return: The model, or None if there is no such model.
        """
        serialized_model = self.dao.retrieve_serialized_model(user_name, model_name)
        print(f"ret {user_name}\n{model_name}\n{serialized_model}")
        if serialized_model is None:
            return None
        return deserialize_from_bytes(serialized_model)

    def store_model(self, user_name, model_name, model):
        """Stores the given model.

        :param user_name: the name of the user who owns the model
        :param model_name: the name of the model
        :param model: the model
        :return: a truthy value if successful, falsy otherwise
        """
        print(f"sto {user_name}\n{model_name}\n{serialize(model)}")
        return self.dao.store_serialized_model(user_name, model_name, serialize(model))


class ModelDao:
    """Data access object for models."""

    def __init__(self, redis_connection: redis.Redis):
        self.rconn = redis_connection

    def retrieve_serialized_model(self, user_name, model_name):
        """Retrieves the serialized model from the database.

        :param user_name: the user who owns the model to retrieve
        :param model_name: the model to retrieve
        :return: JSON, parsable as a model, if the given user has a model with the given name. Returns None if there is
        no model with the given name
        :raise redis.redisError: if there is an issue connecting to the database
        """
        try:
            return self.rconn.get(redis_keys.for_model(user_name, model_name))
        except redis.RedisError as e:
            return None

    def store_serialized_model(self, user_name, model_name, serialized_model):
        """Stores the given model in redis.

        :param user_name: the name of the user who is storing the model
        :param model_name: the name of the model to store
        :param serialized_model:
        :return: a truthy value if storing the model succeeded, falsy if not
        """
        try:
            self.rconn.set(redis_keys.for_model(user_name, model_name), json.dumps(serialized_model))
            return True
        except redis.RedisError as e:
            return False


def deserialize_from_bytes(model_json_as_bytestring):
    return deserialize(json.loads(model_json_as_bytestring.decode("utf8")))


def deserialize_from_string(model_json_as_string):
    return deserialize(json.loads(model_json_as_string))


def deserialize(model_json):
    model_classes = {
        "decision_tree": DecisionTree,
        "random_forest": RandomForest
    }

    try:
        model_type = model_json["model_type"]
        model_class = model_classes[model_type]
        return model_class(model_json)
    except TypeError or AttributeError or KeyError or ValueError as e:
        traceback.print_exc()
        return None


def serialize_to_string(model):
    try:
        return json.dumps(model.data)
    except AttributeError or ValueError or TypeError:
        return None


def serialize(model):
    try:
        return model.data
    except AttributeError:
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
            # Returns as array of length one, containing tuple of item and count, so value is at index [0][0]
            most_common = Counter(predictions).most_common(1)
            return most_common[0][0]

        return predict