from flask import current_app


def authenticate_user(user_name, request):
    pass_hash = request.headers.get("password_hash_sha3_512")
    return current_app.auth.check_credentials(user_name, pass_hash)
