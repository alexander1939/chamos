from flask import Blueprint, jsonify, request, make_response,url_for,flash,redirect, render_template
from app.db.db import db
from app.db.users_model import User
from app.db.session_model import ActiveSession
from datetime import datetime,timedelta
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
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
    
    # 1️⃣ Crear el usuario sin preguntas ni respuestas
    new_user = User(
        email=data["email"],
        password=hashed_password,
        name=data["name"],
        surnames=data["surnames"],
        phone=data["phone"],
        role_id=2
    )
    
    db.session.add(new_user)
    db.session.flush()  # Se usa para obtener el ID del usuario antes de hacer commit

    # 2️⃣ Registrar solo las respuestas sin crear preguntas
    for i in range(1, 3):  # Solo procesamos las 2 preguntas
        pregunta_id = data.get(f"pregunta{i}")  # Obtener el ID de la pregunta seleccionada
        respuesta_texto = data.get(f"respuesta{i}")

        if pregunta_id and respuesta_texto:
            # Crear la respuesta asociada al usuario y la pregunta predefinida
            answer = Answer(user_id=new_user.id, question_id=pregunta_id, response=respuesta_texto)
            db.session.add(answer)

    # 3️⃣ Asignar privilegios al usuario
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

    # Guardar sesión en la base de datos
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

    # Obtener todas las sesiones activas del usuario
    sessions = ActiveSession.query.filter_by(user_id=user.id).all()
    session_list = [
        {
            "id": session.id,
            "ip_address": session.ip_address,
            "user_agent": session.user_agent,
            "created_at": session.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for session in sessions
    ]

    response = jsonify({
        "message": "Login exitoso",
        "redirect_url": url_for('auth.index'),
        "token": token,
        "refresh_token": refresh_token,
        "active_sessions": session_list  # Añadir sesiones activas al response
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

#APi para obtener los datos de la tabla ACtiveSession
@authApi.get('/api/sessions/')
def get_active_sessions():
    token = request.cookies.get("token")
    print("Token recibido:", token)  # Verificar si llega el token

    if not token or token not in active_tokens:
        print("No autorizado: Token no válido")
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    print("ID de usuario obtenido del token:", user_id)

    sessions = ActiveSession.query.filter_by(user_id=user_id).all()
    print("Sesiones encontradas:", sessions)  # Verificar la lista de sesiones

    session_list = [
        {
            "id": session.id,
            "ip_address": session.ip_address,
            "user_agent": session.user_agent,
            "created_at": session.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for session in sessions
    ]
    print("Lista de sesiones para enviar:", session_list)

    return jsonify({"sessions": session_list}), 200


@authApi.delete('/api/sessions/<int:session_id>/')
def delete_session(session_id):
    token = request.cookies.get("token")
    
    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    current_session = ActiveSession.query.filter_by(id=session_id, user_id=user_id).first()

    if not current_session:
        return jsonify({"error": "Sesión no encontrada"}), 404

    # Eliminar la sesión específica
    db.session.delete(current_session)
    db.session.commit()

    # Verificar si quedan más sesiones activas
    active_sessions = ActiveSession.query.filter_by(user_id=user_id).count()
    
    response = jsonify({"message": "Sesión cerrada correctamente"})

    if active_sessions == 0:
        # Si no quedan sesiones activas, eliminar el token
        del active_tokens[token]
        response.set_cookie("token", "", expires=0)
        response.set_cookie("refresh_token", "", expires=0)

    return response, 200