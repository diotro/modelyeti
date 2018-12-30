

version_prefix = '/v1'

def register_api_blueprints(app):
    from .model_management import model_management_blueprint
    app.register_blueprint(model_management_blueprint, url_prefix=version_prefix + "/model_management")

    from yetiserver.api.v1.user_management import user_management_blueprint
    app.register_blueprint(user_management_blueprint, url_prefix=version_prefix + "/user_management")

    from yetiserver.api.v1.model_logs import model_logs_blueprint
    app.register_blueprint(model_logs_blueprint, url_prefix=version_prefix + "/model_log")

    return app