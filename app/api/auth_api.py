from flask import Blueprint, jsonify, request, make_response,url_for,flash,redirect, render_template
from app.db.db import db
from app.db.users_model import User
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

    # 2️⃣ Registrar preguntas y respuestas si existen en los datos
    for i in range(1, 3):
        pregunta_texto = data.get(f"pregunta{i}")
        respuesta_texto = data.get(f"respuesta{i}")

        if pregunta_texto and respuesta_texto:
            # Buscar si la pregunta ya existe
            question = db.session.query(Question).filter_by(text=pregunta_texto).first()
            if not question:
                question = Question(text=pregunta_texto)
                db.session.add(question)
                db.session.flush()  # Obtener el ID de la pregunta

            # Crear la respuesta asociada al usuario y la pregunta
            answer = Answer(user_id=new_user.id, question_id=question.id, response=respuesta_texto)
            db.session.add(answer)

    # 3️⃣ Asignar privilegios al usuario
    privileges = db.session.query(Privilege).filter(
        Privilege.name.in_(["Materias", "Juegos", "Proyectos"])
    ).all()

    for privilege in privileges:
        db.session.add(UserPrivilege(user_id=new_user.id, privilege_id=privilege.id, can_create=1, can_edit=1, can_view=1, can_delete=1))

    db.session.commit()

    return jsonify({"message": "Usuario registrado con privilegios"}), 201

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

    response = jsonify({
        "message": "Login exitoso",
        "redirect_url": url_for('auth.index'),
        "token": token,
        "refresh_token": refresh_token
    })

    response.set_cookie("token", token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME * 24)

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
    response.set_cookie("token", new_access_token, httponly=True, samesite='Lax', max_age=TOKEN_EXPIRATION_TIME)

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


@authApi.post('/api/verificar-correo/')
def verificar_correo():
    data = request.json if request.is_json else request.form.to_dict()

    if 'email' not in data:
        return jsonify({"error": "Correo electrónico requerido"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"error": "Correo no registrado"}), 404

    return jsonify({
        "message": "Correo encontrado",
        "pregunta1": user.pregunta1,
        "pregunta2": user.pregunta2
    }), 200






@authApi.post('/api/verificar-respuestas/')
def verificar_respuestas():
    data = request.json if request.is_json else request.form.to_dict()

    email = data.get("email")
    respuesta1 = data.get("respuesta1")
    respuesta2 = data.get("respuesta2")

    if not email or not respuesta1 or not respuesta2:
        flash("Faltan datos", "danger")  # Mostrar el error en rojo
        return redirect(url_for('recovery.preguntas_seguridad', email=email))  # Redirigir a la misma página

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Correo no registrado", "danger")  # Mostrar el error en rojo
        return redirect(url_for('recovery.preguntas_seguridad', email=email))  # Redirigir a la misma página

    # Comparar respuestas ignorando mayúsculas y espacios extras
    if user.respuesta1.strip().lower() != respuesta1.strip().lower() or \
       user.respuesta2.strip().lower() != respuesta2.strip().lower():
        flash("Respuestas incorrectas", "danger")  # Mostrar el error en rojo
        return redirect(url_for('recovery.preguntas_seguridad', email=email))  # Redirigir a la misma página

    # Generar un token temporal de recuperación
    token = generate_secure_token()
    active_tokens[token] = {
        "user_id": user.id,
        "expires": time.time() + 600  # Expira en 10 minutos
    }

    # Redirigir al usuario a la página de restablecimiento de contraseña
    return redirect(url_for('recovery.restablecer_contrasena', token=token))


@authApi.route('/restablecer-contrasena/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    # Verificar si el token es válido y no ha expirado
    data = active_tokens.get(token)
    if not data or time.time() > data["expires"]:
        flash("El enlace ha expirado o es inválido", "danger")
        return redirect(url_for('recovery.preguntas_seguridad'))  # O una página de error

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not new_password or new_password != confirm_password:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for('authApi.res_contraseña', token=token))

        # Guardar la nueva contraseña en la base de datos
        user = User.query.get(data["user_id"])
        user.password = generate_password_hash(new_password)  # Encripta la nueva contraseña
        db.session.commit()

        # Eliminar el token después del uso
        del active_tokens[token]

        flash("Tu contraseña ha sido restablecida correctamente", "success")
        return redirect(url_for('authApi.login_user'))  # Redirigir al login

    return render_template('/contra/res_contraseña.jinja', token=token)
