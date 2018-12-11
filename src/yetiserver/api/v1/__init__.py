from .model_management import model_management_blueprint

version_prefix = '/v1'

def register_api_blueprints(app):
    app.register_blueprint(model_management_blueprint, url_prefix=version_prefix + "/model_management")

    return app