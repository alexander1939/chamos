import time
from flask import Blueprint, request, render_template, redirect, url_for, flash,make_response
from flask import jsonify, request, render_template
from flask_login import current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.api.auth_api import register_user, login_user, logout_user, protected_route
from app.api.menu_api import get_user_menu
from app.middleware.auth_middleware import  auth_required, complete_2fa_login, generate_2fa_token, generate_secure_token, guest_only, send_2fa_email, store_2fa_session, validate_2fa_token
from app.db.db import db
from app.db.users_model import User
from app.db.session_model import ActiveSession
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from werkzeug.security import generate_password_hash
from app.db.Juegos_model import Juegos
from app.db.Materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.UserPrivilege_model import UserPrivilege
from app.api.menu_api import get_user_menu
from app.api.auth_api import register_user,login_user
from app.middleware.auth_middleware import validate_user_data, check_existing_user,guest_only,TOKEN_EXPIRATION_TIME
from app.middleware.menu_middleware import menu_required, get_privilege_content
from app.db.preguntas_model import Question


auth_bp = Blueprint('auth', __name__)
# Serializer para 2FA
serializer_2fa = URLSafeTimedSerializer('UUr09BTA_9ZGHjl6Mz75FuUn-ftJli7yN2XMyt1myeA', salt='2fa-confirmation')

used_tokens = set()  # Agrega esto en la parte superior del archivo para almacenar tokens usados
two_fa_session_tokens = {}
active_tokens = {}
refresh_tokens = {}

@auth_bp.route('/')
@auth_required
def index(user):  # Acepta el argumento `user`
    """Ruta protegida que muestra la página de inicio solo si el usuario está autenticado"""
    return render_template("index.jinja", user=user)
    

@auth_bp.get('/register/')
@guest_only
def register():
    questions = Question.query.all()  # Obtener todas las preguntas
    preguntas_1 = questions[:3]  # Primeras 3 preguntas
    preguntas_2 = questions[3:6]  # Otras 3 preguntas
    return render_template("auth/register.jinja", preguntas_1=preguntas_1, preguntas_2=preguntas_2)

@auth_bp.post('/register/')
@guest_only
@check_existing_user
def register_post():
    print(request.form)
    form_data = {
        "name": request.form.get('name', '').strip(),
        "surnames": request.form.get('surnames', '').strip(),
        "phone": request.form.get('phone', '').strip(),
        "email": request.form.get('email', '').strip(),
        "password": request.form.get('password', '').strip(),
        "pregunta1": request.form.get('pregunta1', '').strip(),
        "respuesta1": request.form.get('respuesta1', '').strip(),
        "pregunta2": request.form.get('pregunta2', '').strip(),
        "respuesta2": request.form.get('respuesta2', '').strip(),
    }

    print("Datos recibidos:", form_data)

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

        response, status_code = login_user()
        response_json = response.get_json()

        if status_code == 200:
            token = response_json.get("token")
            refresh_token = response_json.get("refresh_token")

            if not token:
                flash("Error al generar token", "danger")
                return redirect(url_for('auth.login'))

            # Generar y almacenar token 2FA
            two_fa_token = generate_2fa_token(form_data["email"])
            store_2fa_session(two_fa_token, token, refresh_token)

            # Enviar correo de confirmación
            if send_2fa_email(form_data["email"], two_fa_token):
                flash('Se ha enviado un correo para confirmar tu inicio de sesión.', 'success')
            else:
                flash('Error al enviar el correo.', 'danger')

            return redirect(url_for('auth.login'))
        else:
            flash(response_json.get("error", "Error al iniciar sesión"), "danger")
            return redirect(url_for('auth.login'))

    return render_template("auth/login.jinja")


@auth_bp.route('/confirm_2fa/<token>', methods=['GET'])
def confirm_2fa(token):
    choice = request.args.get('choice', 'no')

    email = validate_2fa_token(token)
    if not email:
        return redirect(url_for('auth.two_fa_message', message='El enlace de confirmación es inválido o ha expirado.'))

    if choice == 'yes':
        resp = complete_2fa_login(token)
        if resp:
            flash("Inicio de sesión exitoso", "success")
            return resp
        else:
            return redirect(url_for('auth.two_fa_message', message='Error al recuperar los tokens de sesión.'))
    else:
        flash("Inicio de sesión cancelado", "danger")
        return redirect(url_for('auth.two_fa_message', message='Inicio de sesión cancelado.'))

@auth_bp.route('/2fa_message/<message>', methods=['GET'])
def two_fa_message(message):
    """Muestra un mensaje relacionado con el 2FA y redirige al login después de unos segundos."""
    return render_template('auth/2fa_message.jinja', message=message)

@auth_bp.get('/gestionar_privilegios/')
@auth_required
def priv(user):
    return render_template("auth/manage_priv.jinja", user=user)

@auth_bp.route("/contact")
def contact():
    return render_template("contact.jinja")


#Ruta de la vista de sesiones unicas
@auth_bp.route('/active_sessions', methods=['GET'])
@auth_required
def active_sessions(user):
    """Ruta para visualizar sesiones activas del usuario"""
    sessions = ActiveSession.query.filter_by(user_id=user.id).all()
    return render_template("auth/active_sessions.jinja", user=user, sessions=sessions)
