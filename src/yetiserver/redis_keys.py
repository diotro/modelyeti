"""Functions that tell you where to find data in redis."""


def for_model(user_name, model_name):
    return f"models::{user_name}::{model_name}"


def for_user_set():
    return f"users_aggregates::usernames"


def for_user_information(user_name):
    return f"users::{user_name}"


def for_user_password_hash(user_name):
    return f"{for_user_information(user_name)}::password_hash"


def for_user_email(user_name):
    return f"{for_user_information(user_name)}::email"


def for_user_api_keys(user_name):
    return f"{for_user_information(user_name)}::api_keys"


def for_user_billing_info(user_name):
    return f"{for_user_information(user_name)}::billing_information"