from flask import Flask, render_template
from flask_migrate import Migrate
from app.features.components.error_handlers import init_error_handlers
from .config import Config
from flask_login import LoginManager
from .db import db
from .features.auth.routes import auth_bp
from .api.menu_api import menu 
from .api.auth_api import authApi
from .api.materia_api import materia_api
from .api.juego_api import juegos_api
from .api.proyecto_api import proyectos_api
from .api.users_api import usersApi
from .features.components import generate_breadcrumbs, create_roles, create_privileges
from .db.users_model import User
from .features.components.create_admin import create_admin_user
from .features.materia.routes import materia_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 

    init_error_handlers(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Registrar el Blueprint correctamente
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu)  
    app.register_blueprint(authApi)
    app.register_blueprint(materia_api)
    app.register_blueprint(juegos_api)
    app.register_blueprint(proyectos_api)
    app.register_blueprint(usersApi) 
    app.register_blueprint(materia_bp)


    @app.context_processor
    def inject_breadcrumbs():
        return {"breadcrumbs": generate_breadcrumbs()}
    
    @app.errorhandler(410)
    def gone(error):
        return render_template('errors/410.jinja'), 410
    
    with app.app_context():
        db.create_all()
        create_roles()
        create_privileges()
        create_admin_user()

    return app

active_tokens = {}  # Diccionario global para almacenar los tokens activos
