from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask import jsonify, request, render_template
from app.api.auth_api import register_user, login_user, logout_user, protected_route
from app.middleware.auth_middleware import  auth_required
from app.api.menu_api import get_user_menu
from app.middleware.auth_middleware import auth_required, guest_only
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
from app.api.auth_api import register_user,login_user
from app.middleware.auth_middleware import validate_user_data, check_existing_user,guest_only 


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@auth_required
def index():
    return render_template("index.jinja")

@auth_bp.route('/register/', methods=['GET', 'POST'])
@guest_only 
@check_existing_user
def register():
    if request.method == 'POST':
        form_data = {
            "name": request.form.get('name', '').strip(),
            "surnames": request.form.get('surnames', '').strip(),
            "phone": request.form.get('phone', '').strip(),
            "email": request.form.get('email', '').strip(),
            "password": request.form.get('password', '').strip(),
        }

        validation_error = validate_user_data(form_data)
        if validation_error:
            error_json = validation_error.get_json()
            flash(error_json.get("error", "Error desconocido"), "danger")
            return render_template("auth/register.jinja")

        # Llamar a la función de la API para registrar el usuario
        response, status_code = register_user()
        response_json = response.get_json()

        if status_code == 201:
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for('auth.login')) 

        flash(response_json.get("error", "Error al registrar usuario"), "danger")
        return render_template("auth/register.jinja")

    return render_template("auth/register.jinja")



@auth_bp.route('/login/', methods=['GET', 'POST'])
@guest_only
def login():
    if request.method == "POST":
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            return jsonify({"error": "Faltan datos"}), 400

        response = login_user() 
        status_code = response.status_code  

        if status_code == 200:
            return response  
        else:
            return jsonify({"error": "Error al iniciar sesión"}), status_code

    return render_template("auth/login.jinja")




@auth_bp.get('/gestionar_privilegios/')
@auth_required
def priv():
    return render_template("auth/manage_priv.jinja")

