import re
from flask import request, jsonify, redirect, url_for, make_response
from functools import wraps
from app.db.users_model import User
from werkzeug.security import check_password_hash
import uuid
import time

# Token management
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

def auth_required(f):
    """Middleware para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("token")

        if token and is_token_valid(token):
            return f(*args, **kwargs)

        refresh_token = request.cookies.get("refresh_token")
        if refresh_token and refresh_token in refresh_tokens:
            token_data = refresh_tokens[refresh_token]

            if token_data["expires"] > time.time(): 
                new_token = generate_secure_token()
                active_tokens[new_token] = {
                    "user_id": token_data["user_id"],
                    "expires": time.time() + TOKEN_EXPIRATION_TIME
                }

                response = make_response(f(*args, **kwargs))
                response.set_cookie("token", new_token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)
                return response

        return redirect(url_for("auth.login"))  

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