import re
from flask import render_template, request, jsonify, redirect, url_for, make_response,flash
from functools import wraps
from app.db.users_model import User
from app.db.db import db
from werkzeug.security import check_password_hash
import uuid
import time
from flask import redirect, url_for, make_response, flash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

active_tokens = {}
refresh_tokens = {}
TOKEN_EXPIRATION_TIME = 180  # 1 hora

def generate_secure_token():
    """Genera un token único usando UUID"""
    return str(uuid.uuid4())

def is_token_valid(token):
    """Valida si el token existe y no ha expirado"""
    return token in active_tokens and active_tokens[token]["expires"] > time.time()

def validate_user_data(data):
    """Valida los datos del usuario"""
    required_fields = ["email", "password", "name", "surnames", "phone"]
    if not all(field in data and data[field].strip() for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", data["name"]):
        return jsonify({"error": "El nombre solo puede contener letras y espacios."}), 400

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", data["surnames"]):
        return jsonify({"error": "Los apellidos solo pueden contener letras y espacios."}), 400

    if not re.match(r"^\d{10}$", data["phone"]):
        return jsonify({"error": "El teléfono solo puede contener números de 10 dígitos."}), 400

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", data["email"]):
        return jsonify({"error": "El correo electrónico no es válido."}), 400

    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$", data["password"]):
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula y un número."}), 400

    return None

def check_existing_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            data = request.get_json() if request.is_json else request.form

            validation_error = validate_user_data(data)
            if validation_error:
                return validation_error

            existing_user = User.query.filter(
                (User.email == data["email"]) | 
                ((User.name == data["name"]) & (User.surnames == data["surnames"]))
            ).first()

            if existing_user:
                return jsonify({"error": "Ya existe un usuario con este correo, nombre y apellidos."}), 400

        return f(*args, **kwargs)

    return decorated_function

def get_current_user():
    """Obtiene el usuario autenticado a partir del token."""
    token = request.cookies.get("token")

    if not token:
        return None, "Inicie sesion para acceder", 401

    if token not in active_tokens:
        return None, "Token inválido", 401

    # Verificar si el token ha expirado
    if active_tokens[token]["expires"] <= time.time():
        return None, "Token expirado", 401

    user_id = active_tokens[token]["user_id"]
    user = db.session.query(User).filter_by(id=user_id).first()

    if not user:
        return None, "Usuario no encontrado", 404

    return user, None, None


def auth_required(f):
    """Middleware para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.endpoint == "auth.login":
            return f(*args, **kwargs)

        user, error_message, status_code = get_current_user()

        if error_message:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": error_message}), status_code

            flash(error_message, "danger")
            return redirect(url_for("auth.login"))

        return f(user, *args, **kwargs)

    return decorated_function



def guest_only(f):
    """Middleware para evitar que usuarios autenticados accedan a login y registro"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("token")  

        if token and is_token_valid(token):
            return redirect(url_for("auth.index"))  

        return f(*args, **kwargs)

    return decorated_function

# Serializer para 2FA
serializer_2fa = URLSafeTimedSerializer(
    'UUr09BTA_9ZGHjl6Mz75FuUn-ftJli7yN2XMyt1myeA',
    salt='2fa-confirmation'
)

# Diccionarios para manejar sesiones temporales
two_fa_session_tokens = {}

def generate_2fa_token(email):
    """Genera un token seguro para 2FA y lo almacena temporalmente."""
    two_fa_token = serializer_2fa.dumps(email, salt='2fa-confirmation')
    return two_fa_token

def store_2fa_session(token, access_token, refresh_token):
    """Almacena temporalmente el token de sesión para la verificación 2FA."""
    two_fa_session_tokens[token] = {
        "token": access_token,
        "refresh_token": refresh_token,
        "expires": time.time() + 300  # 5 minutos de expiración
    }
    clean_expired_tokens()  # Elimina tokens expirados automáticamente

def clean_expired_tokens():
    """Elimina tokens expirados del diccionario two_fa_session_tokens."""
    current_time = time.time()
    expired_tokens = [token for token, data in two_fa_session_tokens.items() if data.get("expires", 0) <= current_time]
    for token in expired_tokens:
        del two_fa_session_tokens[token]

def send_2fa_email(email, two_fa_token):
    from app import mail
    """Envía un correo con el enlace para confirmar 2FA."""
    confirmation_link = url_for('auth.confirm_2fa', token=two_fa_token, _external=True)
    html_body = render_template('auth/2fa_email.jinja', confirmation_link=confirmation_link)

    msg = Message('Confirmación de inicio de sesión', recipients=[email])
    msg.html = html_body

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f'Error al enviar correo: {e}')
        return False

def validate_2fa_token(token):
    """Valida el token de 2FA y devuelve el email asociado si es válido."""
    try:
        email = serializer_2fa.loads(token, salt='2fa-confirmation', max_age=300)
        return email
    except Exception as e:
        print(f"Error al validar el token: {e}")
        return None

def complete_2fa_login(token):
    """Completa el proceso de inicio de sesión tras la validación de 2FA."""
    session_tokens = two_fa_session_tokens.get(token)
    if not session_tokens:
        return None

    access_token = session_tokens.get("token")
    refresh_token = session_tokens.get("refresh_token")

    # Eliminar tokens temporales después del uso
    del two_fa_session_tokens[token]

    # Crear respuesta con cookies
    resp = make_response(redirect(url_for('auth.index')))
    resp.set_cookie("token", access_token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)
    resp.set_cookie("refresh_token", refresh_token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME * 24)
    
    return resp