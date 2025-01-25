from flask import Flask, render_template
from flask_migrate import Migrate
from app.features.components.error_handlers import init_error_handlers
from .config import Config
from flask_login import LoginManager
from .db import db
from .features.auth import auth
from .features.auth.model import User  # Importa el modelo User
from .features.components import generate_breadcrumbs
from app.features.components import create_admin_user
from .features.materia import materia

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Ruta para el login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 


    init_error_handlers(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(auth)
    app.register_blueprint(materia)

    @app.context_processor
    def inject_breadcrumbs():
        return {"breadcrumbs": generate_breadcrumbs()}

    with app.app_context():
        db.create_all()
        create_admin_user()

    return app
