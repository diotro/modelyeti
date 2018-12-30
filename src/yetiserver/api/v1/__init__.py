

version_prefix = '/v1'

def register_api_blueprints(app):
    from .model_management import model_management_blueprint
    app.register_blueprint(model_management_blueprint, url_prefix=version_prefix + "/model_management")

    from yetiserver.api.v1.user_management_blueprint import user_management_blueprint
    app.register_blueprint(user_management_blueprint, url_prefix=version_prefix + "/user_management")

    return app