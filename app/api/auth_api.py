from flask import jsonify, request, render_template
from app.db.db import db
from app.db.users_model import User
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from werkzeug.security import generate_password_hash
from app.middleware.auth_middleware import check_existing_user
from app.middleware.auth_middleware import generate_secure_token, active_tokens, refresh_tokens, TOKEN_EXPIRATION_TIME,auth_required,is_token_valid
import time
from werkzeug.security import check_password_hash






@check_existing_user
def register_user():
    if request.method == "GET":
        return render_template("auth/register.jinja")

    if request.method == "POST":
        data = request.get_json()

        hashed_password = generate_password_hash(data["password"])
        new_user = User(
            email=data["email"],
            password=hashed_password,
            name=data["name"],
            surnames=data["surnames"],
            phone=data["phone"],
            role_id=2
        )

        db.session.add(new_user)
        db.session.flush()  

        privileges = db.session.query(Privilege).filter(
            Privilege.name.in_(["Materias", "Juegos", "Proyectos"])
        ).all()

        for privilege in privileges:
            db.session.add(UserPrivilege(user_id=new_user.id, privilege_id=privilege.id))

        db.session.commit()

        return jsonify({"message": "Usuario registrado con privilegios"}), 201

def login_user():
    if request.method == "GET":
        return render_template("auth/login.jinja")

    if request.method == "POST":
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), 415

        data = request.get_json()

        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Faltan datos"}), 400

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not check_password_hash(user.password, data["password"]):
            return jsonify({"error": "Credenciales incorrectas"}), 401

        token = generate_secure_token()
        refresh_token = generate_secure_token()

        active_tokens[token] = {
            "user_id": user.id,
            "expires": time.time() + TOKEN_EXPIRATION_TIME
        }

        refresh_tokens[refresh_token] = {  
            "user_id": user.id,
            "expires": time.time() + TOKEN_EXPIRATION_TIME * 24
        }

        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "refresh_token": refresh_token
        }), 200




@auth_required
def logout_user():
    token = request.headers.get("Authorization")

    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]

    if token in active_tokens:
        del active_tokens[token]
        return jsonify({"message": "Sesión cerrada correctamente"}), 200

    return jsonify({"error": "Token inválido"}), 401

@auth_required
def protected_route():
    return jsonify({"message": "Acceso autorizado"}), 200

