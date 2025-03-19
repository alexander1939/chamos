import time
from flask import Blueprint, request, render_template, redirect, url_for, flash,make_response
from flask import jsonify, request, render_template
from flask_login import current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.api.auth_api import register_user, login_user, logout_user, protected_route
from app.api.menu_api import get_user_menu
from app.middleware.auth_middleware import  auth_required, complete_2fa_login, generate_2fa_token, generate_secure_token, guest_only, send_2fa_email, store_2fa_session, validate_2fa_token, is_token_valid, get_active_tokens
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
from app.db.UserSessionSettings_model import UserSessionSettings
from app.api.menu_api import get_user_menu
from app.api.auth_api import register_user,login_user
from app.middleware.auth_middleware import validate_user_data, check_existing_user,guest_only,TOKEN_EXPIRATION_TIME,active_tokens
from app.middleware.menu_middleware import menu_required, get_privilege_content
from app.db.preguntas_model import Question
from werkzeug.security import check_password_hash
from flask import session  # Agrega esto arriba
from datetime import datetime,timedelta



auth_bp = Blueprint('auth', __name__)
serializer_2fa = URLSafeTimedSerializer('UUr09BTA_9ZGHjl6Mz75FuUn-ftJli7yN2XMyt1myeA', salt='2fa-confirmation')

used_tokens = set()  
two_fa_session_tokens = {}
refresh_tokens = {}
temp_session_tokens = {}  

@auth_bp.route('/')
@auth_required
def index(user): 
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

        user = db.session.query(User).filter_by(email=form_data["email"]).first()
        if not user:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for('auth.login'))

        session_settings = db.session.query(UserSessionSettings).filter_by(user_id=user.id).first()
        enable_2fa = session_settings.enable_2fa if session_settings else False
        allow_multiple_sessions = session_settings.allow_multiple_sessions if session_settings else False

        active_sessions = db.session.query(ActiveSession).filter_by(user_id=user.id).count()
        has_active_sessions = active_sessions > 0

        print(f"[DEBUG] Usuario {user.email} tiene sesiones activas: {has_active_sessions}")

        response, status_code = login_user()
        response_json = response.get_json()

        if status_code == 200:
            token = response_json.get("token")
            refresh_token = response_json.get("refresh_token")

            if not token:
                flash("Error al generar token", "danger")
                return redirect(url_for('auth.login'))

            if has_active_sessions and not allow_multiple_sessions:
                temp_token = generate_secure_token()
                temp_session_tokens[temp_token] = {
                    "user_id": user.id,
                    "token": token,
                    "refresh_token": refresh_token,
                    "expires": time.time() + 300  
                }

                return redirect(url_for('auth.confirm_close_sessions', temp_token=temp_token))


            if enable_2fa:
                two_fa_token = generate_2fa_token(form_data["email"])
                store_2fa_session(two_fa_token, token, refresh_token)

                if send_2fa_email(form_data["email"], two_fa_token):
                    flash('Se ha enviado un correo para confirmar tu inicio de sesión.', 'success')
                else:
                    flash('Error al enviar el correo.', 'danger')

                return redirect(url_for('auth.login'))

            print("[DEBUG] Registrando sesión en ActiveSession antes de ir al index...")
            resp = make_response(redirect(url_for('auth.index')))
            resp.set_cookie("token", token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)
            resp.set_cookie("refresh_token", refresh_token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME * 24, path='/')

            flash("Inicio de sesión exitoso", "success")
            return resp

        else:
            flash(response_json.get("error", "Error al iniciar sesión"), "danger")
            return redirect(url_for('auth.login'))

    return render_template("auth/login.jinja")


@auth_bp.route('/confirm_close_sessions/<temp_token>', methods=['GET'])
def confirm_close_sessions(temp_token):
    """Muestra la pantalla de cierre de sesiones si el token es válido."""
    session_data = temp_session_tokens.get(temp_token)

    if not session_data or session_data["expires"] < time.time():
        flash("El enlace de cierre de sesión ha expirado.", "danger")
        return redirect(url_for('auth.login'))

    return render_template("auth/close_sessions.jinja", temp_token=temp_token)

@auth_bp.route('/process_close_sessions', methods=['POST'])
def process_close_sessions():
    temp_token = request.form.get("temp_token")

    if not temp_token or temp_token not in temp_session_tokens:
        flash("Token inválido.", "danger")
        return redirect(url_for('auth.login'))

    session_data = temp_session_tokens.pop(temp_token)  
    user_id = session_data["user_id"]
    final_token = session_data["token"]
    refresh_token = session_data["refresh_token"]

    db.session.query(ActiveSession).filter_by(user_id=user_id).delete()
    db.session.commit()

    tokens_to_remove = [k for k, v in active_tokens.items() if v["user_id"] == user_id]
    for token in tokens_to_remove:
        del active_tokens[token]

    new_session = ActiveSession(
        user_id=user_id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        created_at=datetime.utcnow()
    )

    db.session.add(new_session)
    db.session.commit()

    active_tokens[final_token] = {"user_id": user_id, "session_id": new_session.id, "expires": time.time() + TOKEN_EXPIRATION_TIME}

    resp = make_response(redirect(url_for('auth.index')))
    resp.set_cookie("token", final_token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)
    resp.set_cookie("refresh_token", refresh_token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME * 24, path='/')

    flash("✔️ Todas las sesiones se han cerrado correctamente. Se ha iniciado una nueva sesión.", "success")

    return resp



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


@auth_bp.route('/active_sessions', methods=['GET'])
@auth_required
def active_sessions(user):
    """Ruta para visualizar sesiones activas del usuario"""
    sessions = ActiveSession.query.filter_by(user_id=user.id).all()
    return render_template("auth/active_sessions.jinja", user=user, sessions=sessions)

@auth_bp.route("/session_verification")
def session_verification():
    return render_template("auth/session_verification.jinja")