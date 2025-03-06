import time
from flask import Blueprint, request, render_template, redirect, url_for, flash,make_response
from flask import jsonify, request, render_template
from flask_login import current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from app.api.auth_api import register_user, login_user, logout_user, protected_route
from app.api.menu_api import get_user_menu
from app.middleware.auth_middleware import  auth_required, generate_secure_token, guest_only
from app.db.db import db
from app.db.users_model import User
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

# Serializer para 2FA
serializer_2fa = URLSafeTimedSerializer('UUr09BTA_9ZGHjl6Mz75FuUn-ftJli7yN2XMyt1myeA', salt='2fa-confirmation')

two_fa_session_tokens = {}
active_tokens = {}
refresh_tokens = {}

@auth_bp.route('/login/', methods=['GET', 'POST'])
@guest_only
def login():
    from app import mail
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

            # Generar token temporal para 2FA
            two_fa_token = serializer_2fa.dumps(form_data["email"], salt='2fa-confirmation')

            # Almacenar tokens de sesión temporalmente
            two_fa_session_tokens[two_fa_token] = {
                "token": token,
                "refresh_token": refresh_token,
                "expires": time.time() + 300  # 5 minutos de expiración
            }

            # Limpiar tokens expirados
            clean_expired_tokens()

            print(f"Token generado: {two_fa_token}")  # Debug
            print(f"Tokens almacenados: {two_fa_session_tokens}")  # Debug

            # Crear enlace de confirmación
            confirmation_link = url_for('auth.confirm_2fa', token=two_fa_token, _external=True)

            # Renderizar la plantilla del correo
            html_body = render_template('auth/2fa_email.jinja', confirmation_link=confirmation_link)

            # Enviar correo electrónico
            msg = Message(
                'Confirmación de inicio de sesión',
                recipients=[form_data["email"]]
            )
            msg.html = html_body

            try:
                mail.send(msg)
                flash('Se ha enviado un correo electrónico para confirmar tu inicio de sesión.', 'success')
            except Exception as e:
                flash(f'Error al enviar correo: {e}', 'danger')

            return redirect(url_for('auth.login'))
        else:
            error_message = response_json.get("error", "Error al iniciar sesión")
            flash(error_message, "danger")
            return redirect(url_for('auth.login'))

    return render_template("auth/login.jinja")



@auth_bp.route('/confirm_2fa/<token>', methods=['GET'])
def confirm_2fa(token):
    choice = request.args.get('choice', 'no')  # Por defecto, asumir "No"

    try:
        # Verificar y cargar el token
        email = serializer_2fa.loads(token, salt='2fa-confirmation', max_age=300)  # 5 minutos de expiración
    except Exception as e:
        print(f"Error al validar el token: {e}")  # Debug
        return redirect(url_for('auth.two_fa_message', message='El enlace de confirmación es inválido o ha expirado.'))

    # Verificar si el token existe en el diccionario
    if token not in two_fa_session_tokens:
        return redirect(url_for('auth.two_fa_message', message='El token de confirmación no es válido o ya fue usado.'))

    # Verificar si el token ha expirado
    if two_fa_session_tokens[token].get("expires", 0) <= time.time():
        del two_fa_session_tokens[token]
        return redirect(url_for('auth.two_fa_message', message='El token de confirmación ha expirado.'))

    if choice == 'yes':
        # Recuperar tokens de sesión temporalmente almacenados
        session_tokens = two_fa_session_tokens.get(token)

        if not session_tokens:
            return redirect(url_for('auth.two_fa_message', message='Error al recuperar los tokens de sesión.'))

        token = session_tokens.get("token")
        refresh_token = session_tokens.get("refresh_token")

        if not token:
            return redirect(url_for('auth.two_fa_message', message='Error al generar token.'))

        # 🔹 Crear la respuesta y establecer cookies
        resp = make_response(redirect(url_for('auth.index')))
        resp.set_cookie("token", token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)
        resp.set_cookie("refresh_token", refresh_token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME * 24)

        # Eliminar tokens temporales
        if token in two_fa_session_tokens:
            del two_fa_session_tokens[token]

        flash("Inicio de sesión exitoso", "success")
        return resp
    else:
        # Eliminar tokens temporales si el usuario cancela
        if token in two_fa_session_tokens:
            del two_fa_session_tokens[token]

        # Cerrar la sesión del usuario eliminando las cookies
        resp = make_response(redirect(url_for('auth.two_fa_message', message='Inicio de sesión cancelado.')))
        resp.delete_cookie("token")
        resp.delete_cookie("refresh_token")
        return resp


def clean_expired_tokens():
    """Elimina tokens expirados del diccionario two_fa_session_tokens."""
    current_time = time.time()
    expired_tokens = [token for token, data in two_fa_session_tokens.items() if data.get("expires", 0) <= current_time]
    for token in expired_tokens:
        del two_fa_session_tokens[token]
        print(f"Token expirado eliminado: {token}")  # Debug

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