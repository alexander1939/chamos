from flask import Flask, render_template
from flask_mail import Mail
from flask_migrate import Migrate
from app.features.components.error_handlers import init_error_handlers
from .config import Config
from flask_login import LoginManager
from .db import db
from .features.auth.routes import auth_bp
from .api.menu_api import menu 
from .api.auth_api import authApi
from .api.catalago_api import catalogo_api
from .api.users_api import usersApi
from .features.components import generate_breadcrumbs, create_roles, create_privileges
from .db.users_model import User
from .features.components.create_admin import create_admin_user
from app.features.contra.recovery import recovery_bp
from app.features.router_catalago import catalo_bp
from app.api.search_api import searchApi
from app.features.router_search import search_bp
from app.api.breadcrumbs_api import breadcrumbs_bp

mail = Mail()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'recuperaciondecontrasena7@gmail.com'
    app.config['MAIL_PASSWORD'] = 'oecy hsou xktp kkzh'
    app.config['MAIL_DEFAULT_SENDER'] = 'recuperaciondecontrasena7@gmail.com'

    mail.init_app(app) 

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
    app.register_blueprint(catalogo_api)
    app.register_blueprint(usersApi) 
    app.register_blueprint(catalo_bp)
    app.register_blueprint(searchApi)
    app.register_blueprint(search_bp)
    app.register_blueprint(breadcrumbs_bp)
    app.register_blueprint(recovery_bp, url_prefix='/contra')    


    
    @app.errorhandler(410)
    def gone(error):
        return render_template('errors/410.jinja'), 410
    
    with app.app_context():
        db.create_all()
        create_roles()
        create_privileges()
        create_admin_user()

    return app

active_tokens = {}  
