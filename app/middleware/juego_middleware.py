from functools import wraps
from flask import request, jsonify
import re
from flask import request, jsonify, redirect, url_for
from app.db.users_model import User
from werkzeug.security import check_password_hash
import uuid
import time

def validar_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Obtener token desde headers o cookies
            token = request.headers.get("Authorization")
            if token and token.startswith("Bearer "):
                token = token.split(" ")[1]  # Extraer solo el token real
            else:
                token = request.cookies.get("token")  # Alternativa si viene en cookies

            # Validar si el token es válido
            if not token or token not in active_tokens:
                return jsonify({"error": "Token inválido o no proporcionado"}), 401

            # Adjuntar user_id al request para usarlo en las rutas
            request.user_id = active_tokens[token]["user_id"]

            return f(*args, **kwargs)
        
        except Exception as e:
            return jsonify({"error": "Error en la autenticación", "detalle": str(e)}), 500

    return decorated_function
