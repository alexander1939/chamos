import re
from flask import request, jsonify, redirect, url_for, make_response,flash
from functools import wraps
from app.db.users_model import User
from app.db.db import db
from werkzeug.security import check_password_hash
import uuid
import time

active_tokens = {}
refresh_tokens = {}
TOKEN_EXPIRATION_TIME = 3600  # 1 hora

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
        return None, "Token no proporcionado", 401  

    if token not in active_tokens:
        return None, "Token inválido", 401 

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