# -*- coding: utf-8 -*-
def create_app():
    from flask import Flask
    app = Flask(__name__, instance_relative_config=True)

    from configuration.development import DevelopmentConfig
    app.config.from_object(DevelopmentConfig)
    app.config.from_pyfile("config.py", silent=True)

    from app.model import db
    db.init_app(app)

    from app.views.home import home
    app.register_blueprint(home, url_prefix='')

    return app
