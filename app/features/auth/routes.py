from flask import Blueprint, request, render_template
from flask import jsonify, request, render_template

from app.api.auth_api import register_user, login_user, logout_user, protected_route
from app.middleware.auth_middleware import  auth_required
from app.api.menu_api import get_user_menu
from app.middleware.auth_middleware import generate_secure_token, active_tokens, refresh_tokens, TOKEN_EXPIRATION_TIME,auth_required,is_token_valid
from app.db.db import db
from app.db.users_model import User
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from werkzeug.security import generate_password_hash
from app.db.Juegos_model import Juegos
from app.db.materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.UserPrivilege_model import UserPrivilege
from app.api.menu_api import get_user_menu







auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    """Llama al menú y renderiza la página principal."""
    menu_data = get_user_menu()  # Ahora devuelve un diccionario
    print(f"Datos del menú recibidos: {menu_data}")  # Verifica los datos que estamos pasando
    return render_template("index.jinja", menu=menu_data)



@auth_bp.route('/register/', methods=['GET', 'POST']) 
def register():
    return register_user()

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    return login_user()

@auth_bp.route('/logout/', methods=['POST'])
def logout():
    return logout_user()

@auth_bp.route('/protected/', methods=['GET'])
@auth_required
def protected():
    return protected_route()

