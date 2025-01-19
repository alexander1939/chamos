from flask import Flask, render_template
from flask_migrate import Migrate
from .config import Config
from .db import db
from .features.auth import auth
from .features.components import generate_breadcrumbs

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth)

    @app.context_processor
    def inject_breadcrumbs():
        return {"breadcrumbs": generate_breadcrumbs()}

    with app.app_context():
        db.create_all()

    return app
