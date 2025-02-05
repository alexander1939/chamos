from flask import Blueprint, request, jsonify
from app.db.db import db
from app.db.proyectos_model import Proyectos
from app.middleware.auth_middleware import active_tokens

proyectos_api = Blueprint('proyectos', __name__)  # Cambio en el nombre del Blueprint

@proyectos_api.route('/api/proyectos/agregar', methods=['POST'])  # Cambio en la ruta
def agregar_proyecto():  # Cambio en el nombre de la función
    token = request.cookies.get("token")
    if not token or token not in active_tokens:
        return jsonify({"error": "Token inválido o no proporcionado"}), 401

    user_id = active_tokens[token]["user_id"]
    data = request.get_json()
    nuevo_proyecto = Proyectos(nombre=data['nombre'], descripcion=data['descripcion'], id_usuario=user_id)  # Cambio en el modelo
    db.session.add(nuevo_proyecto)
    db.session.commit()
    return jsonify({"mensaje": "Proyecto agregado correctamente", "id": nuevo_proyecto.id}), 201

@proyectos_api.route('/api/proyectos/listar', methods=['GET'])  
def listar_proyectos():
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
        proyectos = Proyectos.query.filter_by(id_usuario=user_id).all()

        # Si no hay materias
        if not proyectos:
            return jsonify({"message": "No tienes proyectos registrados"}), 200

        # Convertir las materias en formato JSON
        proyectos_data = [{"id": p.id, "nombre": p.nombre, "descripcion": p.descripcion} for p in proyectos]

        return jsonify(proyectos_data), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500
    
    
@proyectos_api.route('/api/proyectos/detalles/<int:proyecto_id>', methods=['GET'])  
def detalles_proyecto(proyecto_id):
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
        proyecto = Proyectos.query.filter_by(id=proyecto_id, id_usuario=user_id).first()

        # Si la materia no existe o no pertenece al usuario
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado o no tienes permiso para verlo"}), 404

        # Crear la respuesta con los detalles de la materia
        proyecto_data = {
            "id": proyecto.id,
            "nombre": proyecto.nombre,
            "descripcion": proyecto.descripcion  # Agrega más atributos si es necesario
        }

        return jsonify(proyecto_data), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500
    
    
@proyectos_api.route('/api/proyectos/eliminar/<int:proyecto_id>', methods=['DELETE'])  
def eliminar_proyecto(proyecto_id):
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
        proyecto = Proyectos.query.filter_by(id=proyecto_id, id_usuario=user_id).first()

        # Si la materia no existe o no pertenece al usuario
        if not proyecto:
            return jsonify({"error": "Proyecto no encontrado o no tienes permiso para eliminarlo"}), 404

        # Eliminar la materia
        db.session.delete(proyecto)
        db.session.commit()

        return jsonify({"message": "Proyecto eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500