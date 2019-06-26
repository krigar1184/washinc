from flask import Flask, g
from werkzeug.contrib.cache import SimpleCache
from wash import views


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.secret_key = 'fq9{_o@P(=0;+g" ('

    if config_overrides:
        app.config.from_mapping(config_overrides)

    app.register_blueprint(views.api)
    app.register_error_handler(404, views.not_found)
    app.cache = SimpleCache()
    app.cache.set('products', {})
    app.cache.set('customers', {})
    app.cache.set('reservations', {})
    app.locks = {
        'products': {},
        'reservations': {},
    }

    return app
