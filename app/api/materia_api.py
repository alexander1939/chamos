from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from app.db.db import db
from app.db.materias_model import Materia
from app.middleware.auth_middleware import active_tokens,is_token_valid
from app.middleware.auth_middleware import auth_required
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
from app.db.users_model import User




materia_api = Blueprint('materias', __name__)  # Cambio en el nombre del Blueprint



@materia_api.get('/api/materias/')
@auth_required
def get_materias():
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401  

    user_id = active_tokens[token]["user_id"]
    current_user = User.query.get(user_id)

    if not current_user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    user_privileges = UserPrivilege.query.filter_by(user_id=current_user.id)\
        .join(Privilege)\
        .filter(Privilege.name == "Materias")\
        .first()

    has_materia_privilege = user_privileges is not None
    can_view = user_privileges.can_view if user_privileges else False

    if not can_view:
        return jsonify({
            "error": "No tienes permiso para ver las materias",
            "has_materia_privilege": has_materia_privilege,
            "can_view": can_view
        }), 403

    materias = Materia.query.all()
    materias_data = [{
        "id": materia.id,
        "nombre": materia.nombre,
        "descripcion": materia.descripcion,
        "id_usuario": materia.id_usuario
    } for materia in materias]

    return jsonify({
        "has_materia_privilege": has_materia_privilege,
        "can_view": can_view,
        "materias": materias_data
    }), 200


@materia_api.route('/api/materias/agregar/', methods=['POST'])  
def add_materia():
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        return jsonify({"error": "No autorizado"}), 401  

    user_id = active_tokens[token]["user_id"]
    current_user = User.query.get(user_id)

    if not current_user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Buscar privilegios del usuario sobre "Materias"
    user_privileges = UserPrivilege.query.filter_by(user_id=current_user.id)\
        .join(Privilege)\
        .filter(Privilege.name == "Materias")\
        .first()

    has_materia_privilege = user_privileges is not None
    can_create = user_privileges.can_create if user_privileges else False

    # Si no tiene permiso can_create, no permitir agregar materia
    if not can_create:
        return jsonify({
            "error": "No tienes permiso para agregar materias",
            "has_materia_privilege": has_materia_privilege,
            "can_create": can_create
        }), 403

    # Obtener datos del request
    data = request.get_json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    if not nombre:
        return jsonify({"error": "El nombre de la materia es obligatorio"}), 400

    # Crear nueva materia
    nueva_materia = Materia(
        nombre=nombre,
        descripcion=descripcion,
        id_usuario=current_user.id
    )

    db.session.add(nueva_materia)
    db.session.commit()

    return jsonify({
        "message": "Materia agregada exitosamente",
        "has_materia_privilege": has_materia_privilege,
        "can_create": can_create,
        "materia": {
            "id": nueva_materia.id,
            "nombre": nueva_materia.nombre,
            "descripcion": nueva_materia.descripcion,
            "id_usuario": nueva_materia.id_usuario
        }
    }), 201

@materia_api.route('/api/materias/<int:materia_id>/', methods=['PUT'])
def edit_materia_simple(materia_id):
    # Obtener el token del header
    auth_header = request.headers.get("Authorization")
    token = auth_header.replace("Bearer ", "") if auth_header else None

    if not token or not is_token_valid(token):
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    current_user = User.query.get(user_id)

    if not current_user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Buscar privilegios del usuario sobre "Materias"
    user_privileges = UserPrivilege.query.filter_by(user_id=current_user.id) \
        .join(Privilege) \
        .filter(Privilege.name == "Materias") \
        .first()

    has_materia_privilege = user_privileges is not None
    can_edit = user_privileges.can_edit if user_privileges else False

    # Verificar si tiene el privilegio de editar materias
    if not can_edit:
        return jsonify({
            "error": "No tienes permiso para editar materias",
            "has_materia_privilege": has_materia_privilege,
            "can_edit": can_edit
        }), 403

    # Buscar la materia a editar
    materia = Materia.query.get(materia_id)
    if not materia:
        return jsonify({"error": "Materia no encontrada"}), 404

    # Obtener datos del request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos no válidos"}), 400

    # Actualizar los valores permitiendo nulos opcionales
    materia.nombre = data.get("nombre", materia.nombre)
    materia.descripcion = data.get("descripcion", materia.descripcion)

    db.session.commit()

    return jsonify({
        "message": "Materia editada exitosamente",
        "materia": {
            "id": materia.id,
            "nombre": materia.nombre,
            "descripcion": materia.descripcion,
            "id_usuario": materia.id_usuario
        }
    }), 200


@materia_api.route('/api/materias/<int:materia_id>/', methods=['DELETE'])
@auth_required
def delete_materia(materia_id):
    auth_header = request.headers.get("Authorization")
    token = auth_header.replace("Bearer ", "") if auth_header else None

    if not token or not is_token_valid(token):
        return jsonify({"error": "No autorizado"}), 401

    user_id = active_tokens[token]["user_id"]
    current_user = User.query.get(user_id)

    if not current_user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    user_privileges = UserPrivilege.query.filter_by(user_id=current_user.id) \
        .join(Privilege) \
        .filter(Privilege.name == "Materias") \
        .first()

    can_delete = user_privileges.can_delete if user_privileges else False

    if not can_delete:
        return jsonify({"error": "No tienes permiso para eliminar materias"}), 403

    materia = Materia.query.get(materia_id)
    if not materia:
        return jsonify({"error": "Materia no encontrada"}), 404

    db.session.delete(materia)
    db.session.commit()

    return jsonify({"message": "Materia eliminada exitosamente"}), 200
