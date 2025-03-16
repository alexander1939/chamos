from flask import Blueprint, jsonify, request, make_response,url_for,flash,redirect, render_template
from app.db.db import db
from app.db.users_model import User
from app.db.session_model import ActiveSession
from datetime import datetime,timedelta
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from app.db.UserSessionSettings_model import UserSessionSettings
from app.db.preguntas_model import Question
from app.db.respuesta_model import Answer
from werkzeug.security import generate_password_hash, check_password_hash
from app.middleware.auth_middleware import (
    check_existing_user, generate_secure_token, active_tokens, refresh_tokens, 
    TOKEN_EXPIRATION_TIME
)
import time

authApi = Blueprint('authApi', __name__)
 
@authApi.post('/api/register/')
@check_existing_user
def register_user():
    data = request.json if request.is_json else request.form.to_dict()

    hashed_password = generate_password_hash(data["password"])
    
    # 1️⃣ Crear el usuario
    new_user = User(
        email=data["email"],
        password=hashed_password,
        name=data["name"],
        surnames=data["surnames"],
        phone=data["phone"],
        role_id=2
    )
    
    db.session.add(new_user)
    db.session.flush()  # Se usa flush() para obtener el ID del usuario antes de commit

    # 2️⃣ Crear la configuración de sesión con valores predeterminados (sin 2FA y sin múltiples sesiones)
    session_settings = UserSessionSettings(
        user_id=new_user.id,
        allow_multiple_sessions=False,  # ❌ No permite múltiples sesiones por defecto
        enable_2fa=False  # ❌ No activa 2FA por defecto
    )
    db.session.add(session_settings)

    # 3️⃣ Agregar preguntas de seguridad
    for i in range(1, 3):  
        pregunta_id = data.get(f"pregunta{i}")  
        respuesta_texto = data.get(f"respuesta{i}")

        if pregunta_id and respuesta_texto:
            answer = Answer(user_id=new_user.id, question_id=pregunta_id, response=respuesta_texto)
            db.session.add(answer)

    # 4️⃣ Asignar privilegios
    privileges = db.session.query(Privilege).filter(
        Privilege.name.in_(["Materias", "Juegos", "Proyectos"])
    ).all()

    for privilege in privileges:
        db.session.add(UserPrivilege(user_id=new_user.id, privilege_id=privilege.id, can_create=1, can_edit=1, can_view=1, can_delete=1))

    # 5️⃣ Confirmar todos los cambios en la base de datos
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

    ip_address = request.remote_addr  
    user_agent = request.headers.get('User-Agent', 'Desconocido')

    new_session = ActiveSession(
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
        created_at=datetime.utcnow()
    )

    db.session.add(new_session)
    db.session.commit()

    active_tokens[token] = {
        "user_id": user.id,
        "session_id": new_session.id,  
        "expires": time.time() + TOKEN_EXPIRATION_TIME
    }

    response = jsonify({
        "message": "Login exitoso",
        "token": token,
        "refresh_token": refresh_token,
        "user_id": user.id 
    })

    response.set_cookie("token", token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME, path='/')
    response.set_cookie("refresh_token", refresh_token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME * 24, path='/')

    return response, 200


@authApi.post('/api/refresh/')
def refresh_access_token():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token or refresh_token not in refresh_tokens:
        return jsonify({"error": "Refresh token inválido"}), 401

    token_data = refresh_tokens[refresh_token]
    if token_data["expires"] < time.time(): 
        del refresh_tokens[refresh_token]
        return jsonify({"error": "Refresh token expirado, inicie sesión nuevamente"}), 401

    new_access_token = generate_secure_token()
    active_tokens[new_access_token] = {
        "user_id": token_data["user_id"],
        "expires": time.time() + TOKEN_EXPIRATION_TIME
    }

    response = make_response(jsonify({"token": new_access_token}), 200)
    response.set_cookie("token", new_access_token, httponly=False, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)

    return response

@authApi.post('/api/logout/')
def logout_user():
    token = request.cookies.get("token")

    if token in active_tokens:
        del active_tokens[token]

    response = jsonify({"message": "Sesión cerrada correctamente"})
    response.set_cookie("token", "", expires=0)  
    response.set_cookie("refresh_token", "", expires=0)  

    return response, 200

@authApi.get('/api/protected/')
def protected_route():
    return jsonify({"message": "Acceso autorizado"}), 200


@authApi.get('/api/auth/user/')
def get_user():
    token = request.cookies.get("token")
    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "surnames": user.surnames,
        "phone": user.phone
    }), 200

@authApi.delete('/api/sessions/')
def delete_all_sessions_except_current():
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    current_session_id = active_tokens[token]["session_id"]

    sessions_to_delete = ActiveSession.query.filter(
        ActiveSession.user_id == user_id,
        ActiveSession.id != current_session_id
    ).all()

    for session in sessions_to_delete:
        db.session.delete(session)

        for tok, data in list(active_tokens.items()):
            if data["user_id"] == user_id and data["session_id"] == session.id:
                del active_tokens[tok]

    db.session.commit()

    return jsonify({"message": "Todas las sesiones han sido cerradas excepto la actual"}), 200


@authApi.delete('/api/sessions/<int:session_id>/')
def delete_session(session_id):
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    session = ActiveSession.query.filter_by(id=session_id, user_id=user_id).first()

    if not session:
        return jsonify({"error": "Sesión no encontrada"}), 404

    db.session.delete(session)
    db.session.commit()

    # Eliminar todas las entradas del diccionario active_tokens relacionadas con la sesión eliminada
    for tok in list(active_tokens.keys()):
        if active_tokens[tok].get("session_id") == session_id:
            del active_tokens[tok]

    response = jsonify({"message": "Sesión cerrada correctamente"})

    # Antes de acceder a active_tokens[token], asegurarse de que el token sigue existiendo
    if token in active_tokens and session_id == active_tokens[token].get("session_id"):
        del active_tokens[token]
        response.set_cookie("token", "", expires=0, path="/")
        response.set_cookie("refresh_token", "", expires=0, path="/")

    return response, 200

@authApi.get('/api/active/')
def get_active_sessions():
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    sessions = ActiveSession.query.filter_by(user_id=user_id).all()

    sessions_data = [{
        "id": session.id,
        "ip_address": session.ip_address,
        "user_agent": session.user_agent,
        "created_at": session.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for session in sessions]

    return jsonify(sessions_data), 200



@authApi.get('/api/session-settings/')
def get_session_settings():
    token = request.cookies.get("token")
    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    settings = db.session.query(UserSessionSettings).filter_by(user_id=user_id).first()

    if not settings:
        return jsonify({"error": "Configuración de sesión no encontrada"}), 404

    return jsonify({
        "allow_multiple_sessions": settings.allow_multiple_sessions,
        "enable_2fa": settings.enable_2fa
    }), 200


@authApi.put('/api/session-settings/multiple-sessions/')
def update_multiple_sessions():
    token = request.cookies.get("token")
    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    data = request.get_json()

    if "allow_multiple_sessions" not in data:
        return jsonify({"error": "Falta el valor de allow_multiple_sessions"}), 400

    settings = db.session.query(UserSessionSettings).filter_by(user_id=user_id).first()
    if not settings:
        return jsonify({"error": "Configuración de sesión no encontrada"}), 404

    settings.allow_multiple_sessions = bool(data["allow_multiple_sessions"])
    db.session.commit()

    return jsonify({"message": "Configuración actualizada", "allow_multiple_sessions": settings.allow_multiple_sessions}), 200


@authApi.put('/api/session-settings/enable-2fa/')
def update_enable_2fa():
    token = request.cookies.get("token")
    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    data = request.get_json()

    if "enable_2fa" not in data:
        return jsonify({"error": "Falta el valor de enable_2fa"}), 400

    settings = db.session.query(UserSessionSettings).filter_by(user_id=user_id).first()
    if not settings:
        return jsonify({"error": "Configuración de sesión no encontrada"}), 404

    settings.enable_2fa = bool(data["enable_2fa"])
    db.session.commit()

    return jsonify({"message": "Configuración actualizada", "enable_2fa": settings.enable_2fa}), 200