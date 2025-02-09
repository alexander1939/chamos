from functools import wraps
from flask import request, jsonify
from app.db.users_model import User
from app.middleware.auth_middleware import is_token_valid, active_tokens

def user_or_admin_required(f):
    """Middleware que permite a los usuarios ver su info y a los admins ver todos los usuarios normales"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("token")

        if not token or not is_token_valid(token):
            return jsonify({"error": "Token inválido o expirado"}), 401

        user_id = active_tokens[token]["user_id"]
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return f(user, *args, **kwargs)

    return decorated_function


def admin_required(f):
    """Middleware para restringir acceso solo a administradores"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("token")

        if not token or not is_token_valid(token):
            return jsonify({"error": "Token inválido o expirado"}), 401

        user_id = active_tokens[token]["user_id"]
        user = User.query.get(user_id)

        if not user or user.role.name != "Admin":
            return jsonify({"error": "Acceso denegado. Solo administradores pueden acceder a esta ruta."}), 403

        return f(*args, **kwargs)

    return decorated_function