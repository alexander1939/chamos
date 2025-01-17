from flask import Flask, render_template, url_for
from flask_migrate import Migrate
from .config import Config
from .db import db
from .features.auth import auth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth)

    

    with app.app_context():
        db.create_all()

    return app

