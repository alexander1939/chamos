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

@auth_bp.get('/register/')
@guest_only
def register():
    return render_template("auth/register.jinja")


@auth_bp.post('/register/')
@guest_only
@check_existing_user
def register_post():
    form_data = {
        "name": request.form.get('name', '').strip(),
        "surnames": request.form.get('surnames', '').strip(),
        "phone": request.form.get('phone', '').strip(),
        "email": request.form.get('email', '').strip(),
        "password": request.form.get('password', '').strip(),
    }

    validation_error = validate_user_data(form_data)
    if validation_error:
        error_json, status_code = validation_error.get_json(), validation_error.status_code
        flash(error_json.get("error", "Error desconocido"), "danger")
        return render_template("auth/register.jinja"), status_code

    response, status_code = register_user()
    response_json = response.get_json()

    if status_code == 201:
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for('auth.login'))

    flash(response_json.get("error", "Error al registrar usuario"), "danger")
    return render_template("auth/register.jinja")


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        form_data = {
            "email": request.form.get('email', '').strip(),
            "password": request.form.get('password', '').strip(),
        }

        if not form_data["email"] or not form_data["password"]:
            flash("Faltan datos", "danger")
            return redirect(url_for('auth.login'))

        # Llamar a la API para iniciar sesión
        response = login_user()

        if isinstance(response, tuple):
            response_json, status_code = response  
        else:
            status_code = response.status_code
            try:
                response_json = response.json
            except Exception:
                response_json = {"error": "Respuesta inesperada del servidor"}

        if status_code == 200:
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('auth.index'))  # 🔹 Redirección correcta
        else:
            error_message = response_json.get("error", "Error al iniciar sesión")
            flash(error_message, "danger")
            return redirect(url_for('auth.login'))  # 🔹 Redirige con el mensaje de error

    return render_template("auth/login.jinja")


@auth_bp.get('/gestionar_privilegios/')
@auth_required
def priv():
    return render_template("auth/manage_priv.jinja")

