from flask import Blueprint, request, render_template, redirect, url_for, flash,make_response
from flask import jsonify, request, render_template
from app.api.auth_api import register_user, login_user, logout_user, protected_route
from app.api.menu_api import get_user_menu
from app.middleware.auth_middleware import  auth_required, guest_only
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
from app.middleware.auth_middleware import validate_user_data, check_existing_user,guest_only,TOKEN_EXPIRATION_TIME
from app.middleware.menu_middleware import menu_required, get_privilege_content



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@auth_required
def index(user):  # Acepta el argumento `user`
    """Ruta protegida que muestra la página de inicio solo si el usuario está autenticado"""
    return render_template("index.jinja", user=user)

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
@guest_only
def login():
    if request.method == "POST":
        print("🔹 login() ha sido llamado")  # Debug

        form_data = {
            "email": request.form.get('email', '').strip(),
            "password": request.form.get('password', '').strip(),
        }

        if not form_data["email"] or not form_data["password"]:
            flash("Faltan datos", "danger")
            return redirect(url_for('auth.login'))

        # Llamar a la API de login
        response, status_code = login_user()
        response_json = response.get_json()

        print(f"🔹 Respuesta de login_user(): {response_json}")  # Debug

        if status_code == 200:
            token = response_json.get("token")
            refresh_token = response_json.get("refresh_token")

            if not token:
                flash("Error al generar token", "danger")
                return redirect(url_for('auth.login'))

            # 🔹 Crear la respuesta y establecer cookies
            resp = make_response(redirect(url_for('auth.index')))
            resp.set_cookie("token", token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)
            resp.set_cookie("refresh_token", refresh_token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME * 24)

            flash("Inicio de sesión exitoso", "success")
            return resp

        error_message = response_json.get("error", "Error al iniciar sesión")
        flash(error_message, "danger")
        return redirect(url_for('auth.login'))

    return render_template("auth/login.jinja")


@auth_bp.get('/gestionar_privilegios/')
@auth_required
def priv(user):
    return render_template("auth/manage_priv.jinja", user=user)
