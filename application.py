import os
from flask import Flask
from api.models import db
from api.auth import auth
from api.decorators import json, etag
from api.errors import not_found, not_allowed
from api.v1 import api as api_blueprint

application = Flask(__name__)
application.config.from_object('config')

db.init_app(application)

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


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
