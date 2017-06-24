import os
from flask import Flask
from .models import db
from .auth import auth
from .decorators import json, etag
from .errors import not_found, not_allowed


def create_app(config_module=None):
    application = Flask(__name__)
    application.config.from_object(config_module or
                           os.environ.get('FLASK_CONFIG') or
                           'config')

    db.init_app(application)

    from api.v1 import api as api_blueprint
    application.register_blueprint(api_blueprint, url_prefix='/v1')

    if application.config['USE_TOKEN_AUTH']:
        from api.token import token as token_blueprint
        application.register_blueprint(token_blueprint, url_prefix='/auth')

    @application.route('/')
    @auth.login_required
    @etag
    @json
    def index():
        from api.v1 import get_catalog as v1_catalog
        return {'versions': {'v1': v1_catalog()}}

    @application.errorhandler(404)
    @auth.login_required
    def not_found_error(e):
        return not_found('item not found')

    @application.errorhandler(405)
    def method_not_allowed_error(e):
        return not_allowed()

    return application
