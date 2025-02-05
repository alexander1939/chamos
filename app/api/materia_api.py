from flask import Blueprint, request, jsonify
from app.db.db import db
from app.db.Materias_model import Materia
from app.middleware.auth_middleware import active_tokens

materia_api = Blueprint('materias', __name__)  # Cambio en el nombre del Blueprint

@materia_api.route('/api/materias/agregar', methods=['POST'])  # Cambio en la ruta
def agregar_materia():  # Cambio en el nombre de la función
    token = request.cookies.get("token")
    if not token or token not in active_tokens:
        return jsonify({"error": "Token inválido o no proporcionado"}), 401

    user_id = active_tokens[token]["user_id"]
    data = request.get_json()
    nueva_materia = Materia(nombre=data['nombre'], descripcion=data['descripcion'], id_usuario=user_id)  # Cambio en el modelo
    db.session.add(nueva_materia)
    db.session.commit()
    return jsonify({"mensaje": "Materia agregada correctamente", "id": nueva_materia.id}), 201

@materia_api.route('/api/materias/listar', methods=['GET'])
def listar_materias():
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

        # Obtener las materias asociadas al usuario
        materias = Materia.query.filter_by(id_usuario=user_id).all()

        # Si no hay materias
        if not materias:
            return jsonify({"message": "No tienes materias registradas"}), 200

        # Convertir las materias en formato JSON
        materias_data = [{"id": m.id, "nombre": m.nombre} for m in materias]

        return jsonify(materias_data), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500


@materia_api.route('/api/materias/detalles/<int:materia_id>', methods=['GET'])
def detalles_materia(materia_id):
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

        # Buscar la materia en la base de datos y verificar que pertenece al usuario
        materia = Materia.query.filter_by(id=materia_id, id_usuario=user_id).first()

        # Si la materia no existe o no pertenece al usuario
        if not materia:
            return jsonify({"error": "Materia no encontrada o no tienes permiso para verla"}), 404

        # Crear la respuesta con los detalles de la materia
        materia_data = {
            "id": materia.id,
            "nombre": materia.nombre,
            "descripcion": materia.descripcion  # Agrega más atributos si es necesario
        }

        return jsonify(materia_data), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500


@materia_api.route('/api/materias/eliminar/<int:materia_id>', methods=['DELETE'])
def eliminar_materia(materia_id):
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

        # Buscar la materia en la base de datos y verificar que pertenece al usuario
        materia = Materia.query.filter_by(id=materia_id, id_usuario=user_id).first()

        # Si la materia no existe o no pertenece al usuario
        if not materia:
            return jsonify({"error": "Materia no encontrada o no tienes permiso para eliminarla"}), 404

        # Eliminar la materia
        db.session.delete(materia)
        db.session.commit()

        return jsonify({"message": "Materia eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500
