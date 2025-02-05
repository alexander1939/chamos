from flask import Blueprint, request, jsonify
from app.db.db import db
from app.db.Juegos_model import Juegos
from app.middleware.auth_middleware import active_tokens

juegos_api = Blueprint('juegos', __name__)

@juegos_api.route('/api/juegos/agregar', methods=['POST'])
def agregar_juego():
    token = request.cookies.get("token")
    if not token or token not in active_tokens:
        return jsonify({"error": "Token inválido o no proporcionado"}), 401

    user_id = active_tokens[token]["user_id"]
    data = request.get_json()
    nuevo_juego = Juegos(nombre=data['nombre'], descripcion=data['descripcion'], id_usuario=user_id)
    db.session.add(nuevo_juego)
    db.session.commit()
    return jsonify({"mensaje": "Juego agregado correctamente", "id": nuevo_juego.id}), 201

@juegos_api.route('/api/juegos/listar', methods=['GET'])
def listar_juegos():
    try:
        # Obtener token desde headers o cookies
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1]  # Extrae solo el token real
        else:
            token = request.cookies.get("token")  # Alternativa si viene en cookies

        # Validar si el token es válido
        if not token or token not in active_tokens:
            return jsonify({"error": "Token inválido o no proporcionado"}), 401

        user_id = active_tokens[token]["user_id"]

        # Consultar los juegos del usuario en la base de datos
        juegos = Juegos.query.filter_by(id_usuario=user_id).all()

        # Verificar si hay juegos registrados
        if not juegos:
            return jsonify({"mensaje": "No se encontraron juegos para este usuario"}), 200

        # Crear la lista de juegos para la respuesta JSON
        juegos_list = [{"id": j.id, "nombre": j.nombre, "descripcion": j.descripcion} for j in juegos]

        return jsonify(juegos_list), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500
    

@juegos_api.route('/api/juegos/detalles/<int:juego_id>', methods=['GET'])
def detalles_juego(juego_id):
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

        user_id = active_tokens[token]["user_id"]

        # Buscar el juego en la base de datos y verificar que pertenece al usuario
        juego = Juegos.query.filter_by(id=juego_id, id_usuario=user_id).first()

        # Si el juego no existe o no pertenece al usuario
        if not juego:
            return jsonify({"error": "Juego no encontrado o no tienes permiso para verlo"}), 404

        # Crear la respuesta con los detalles del juego
        juego_data = {
            "id": juego.id,
            "nombre": juego.nombre,
            "descripcion": juego.descripcion
        }

        return jsonify(juego_data), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500


@juegos_api.route('/api/juegos/eliminar/<int:juego_id>', methods=['DELETE'])
def eliminar_juego(juego_id):
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

        user_id = active_tokens[token]["user_id"]

        # Buscar el juego en la base de datos y verificar que pertenece al usuario
        juego = Juegos.query.filter_by(id=juego_id, id_usuario=user_id).first()

        # Si el juego no existe o no pertenece al usuario
        if not juego:
            return jsonify({"error": "Juego no encontrado o no tienes permiso para eliminarlo"}), 404

        # Eliminar el juego
        db.session.delete(juego)
        db.session.commit()

        return jsonify({"message": "Juego eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500
