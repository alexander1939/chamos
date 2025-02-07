from flask import Blueprint, jsonify, request, make_response,url_for
from app.db.db import db
from app.db.users_model import User
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from werkzeug.security import generate_password_hash, check_password_hash
from app.middleware.auth_middleware import (
    check_existing_user, generate_secure_token, active_tokens, refresh_tokens, 
    TOKEN_EXPIRATION_TIME, auth_required
)
import time

authApi = Blueprint('authApi', __name__)

@authApi.post('/api/register/')
@check_existing_user
def register_user():
    data = request.json if request.is_json else request.form.to_dict()

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
        db.session.add(UserPrivilege(user_id=new_user.id, privilege_id=privilege.id, can_create=1, can_edit=1, can_view=1, can_delete=1))

    db.session.commit()
    
    return jsonify({"message": "Usuario registrado con privilegios"}), 201  


@authApi.post('/api/login/')
def login_user():
    data = request.json if request.is_json else request.form.to_dict()

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

    response = make_response(jsonify({
        "message": "Login exitoso",
        "token": token,
        "refresh_token": refresh_token
    }), 200)

    response.set_cookie("token", token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME * 24)

    return response



@authApi.post('/api/refresh/')
def refresh_access_token():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token or refresh_token not in refresh_tokens:
        return jsonify({"error": "Refresh token inválido"}), 401

    token_data = refresh_tokens[refresh_token]
    if token_data["expires"] < time.time(): 
        del refresh_tokens[refresh_token]
        return jsonify({"error": "Refresh token expirado, inicie sesión nuevamente"}), 401

    # Generar un nuevo access token
    new_access_token = generate_secure_token()
    active_tokens[new_access_token] = {
        "user_id": token_data["user_id"],
        "expires": time.time() + TOKEN_EXPIRATION_TIME
    }

    response = make_response(jsonify({"token": new_access_token}), 200)
    response.set_cookie("token", new_access_token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)

    return response

@authApi.post('/api/logout/')
@auth_required
def logout_user():
    token = request.cookies.get("token")

    if token in active_tokens:
        del active_tokens[token]

    response = jsonify({"message": "Sesión cerrada correctamente"})
    response.set_cookie("token", "", expires=0)  
    response.set_cookie("refresh_token", "", expires=0)  

    return response, 200

@authApi.get('/api/protected/')
@auth_required
def protected_route():
    return jsonify({"message": "Acceso autorizado"}), 200