from flask import Blueprint, request, jsonify
from app.db.Materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.Juegos_model import Juegos
from app.middleware.catalogo_middleware import get_user_from_token, has_access_to_module, verify_create_permission, verify_edit_permission, verify_delete_permission
from app.db.db import db

catalogo_api = Blueprint('catalogo', __name__)

@catalogo_api.get('/api/catalogo/')
def get_user_catalog():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token no proporcionado."}), 400

    user = get_user_from_token(token)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    modulo = request.args.get('modulo')
    if not modulo:
        return jsonify({"error": "Debe especificar un módulo para ver."}), 400

    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        return jsonify({"error": error}), 403

    try:
        if modulo == 'Materias':
            materias = db.session.query(Materia).filter_by(id_usuario=user.id).all()
            return jsonify({
                "modulo": "Materias",
                "can_create": user_privilege.can_create,
                "can_edit": user_privilege.can_edit,
                "can_view": user_privilege.can_view,
                "can_delete": user_privilege.can_delete,
                "materias": [{"id": materia.id, "nombre": materia.nombre, "descripcion": materia.descripcion} for materia in materias]
    })

        elif modulo == 'Proyectos':
            proyectos = db.session.query(Proyectos).filter_by(id_usuario=user.id).all()
            return jsonify({
                "modulo": "Proyectos",
                "can_create": user_privilege.can_create,
                "can_edit": user_privilege.can_edit,
                "can_view": user_privilege.can_view,
                "can_delete": user_privilege.can_delete,
                "proyectos": [{"id": proyecto.id,"nombre": proyecto.nombre, "descripcion": proyecto.descripcion} for proyecto in proyectos]
            })

        elif modulo == 'Juegos':
            juegos = db.session.query(Juegos).filter_by(id_usuario=user.id).all()
            return jsonify({
                "modulo": "Juegos",
                "can_create": user_privilege.can_create,
                "can_edit": user_privilege.can_edit,
                "can_view": user_privilege.can_view,
                "can_delete": user_privilege.can_delete,
                "juegos": [{"id": juego.id,"nombre": juego.nombre, "descripcion": juego.descripcion} for juego in juegos]
            })

        else:
            return jsonify({"error": "Módulo no válido."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@catalogo_api.get('/api/catalogo/detalle/')
def get_catalogo_detalle():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token no proporcionado."}), 400

    user = get_user_from_token(token)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    modulo = request.args.get('modulo')
    if not modulo:
        return jsonify({"error": "Debe especificar un módulo."}), 400

    data = request.get_json()
    if not data or "id" not in data:
        return jsonify({"error": "Debe proporcionar un ID en el cuerpo de la solicitud."}), 400

    item_id = data["id"]

    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        return jsonify({"error": error}), 403

    try:
        if modulo == 'Materias':
            materia = db.session.query(Materia).filter_by(id=item_id, id_usuario=user.id).first()
            if not materia:
                return jsonify({"error": "Materia no encontrada."}), 404
            return jsonify({
                "modulo": "Materias",
                "can_view": user_privilege.can_view,
                "detalle": {
                    "id": materia.id,
                    "nombre": materia.nombre,
                    "descripcion": materia.descripcion
                }
            })

        elif modulo == 'Proyectos':
            proyecto = db.session.query(Proyectos).filter_by(id=item_id, id_usuario=user.id).first()
            if not proyecto:
                return jsonify({"error": "Proyecto no encontrado."}), 404
            return jsonify({
                "modulo": "Proyectos",
                "can_view": user_privilege.can_view,
                "detalle": {
                    "id": proyecto.id,
                    "nombre": proyecto.nombre,
                    "descripcion": proyecto.descripcion
                }
            })

        elif modulo == 'Juegos':
            juego = db.session.query(Juegos).filter_by(id=item_id, id_usuario=user.id).first()
            if not juego:
                return jsonify({"error": "Juego no encontrado."}), 404
            return jsonify({
                "modulo": "Juegos",
                "can_view": user_privilege.can_view,
                "detalle": {
                    "id": juego.id,
                    "nombre": juego.nombre,
                    "descripcion": juego.descripcion
                }
            })

        else:
            return jsonify({"error": "Módulo no válido."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@catalogo_api.post('/api/catalogo/agregar/')
def add_new_content():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token no proporcionado."}), 400

    user = get_user_from_token(token)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    modulo = request.args.get('modulo')
    if not modulo:
        return jsonify({"error": "Debe especificar un módulo para agregar contenido."}), 400

    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        return jsonify({"error": error}), 403

    permission_error = verify_create_permission(user_privilege)
    if permission_error:
        return permission_error

    data = request.json
    try:
        if modulo == 'Materias':
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')

            if not nombre or not descripcion:
                return jsonify({"error": "Debe proporcionar nombre y descripción."}), 400

            nueva_materia = Materia(nombre=nombre, descripcion=descripcion, id_usuario=user.id)
            db.session.add(nueva_materia)
            db.session.commit()

            return jsonify({"message": "Materia creada con éxito", "materia": {"nombre": nombre, "descripcion": descripcion}}), 201

        elif modulo == 'Proyectos':
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')

            if not nombre or not descripcion:
                return jsonify({"error": "Debe proporcionar nombre y descripción."}), 400

            nuevo_proyecto = Proyectos(nombre=nombre, descripcion=descripcion, id_usuario=user.id)
            db.session.add(nuevo_proyecto)
            db.session.commit()

            return jsonify({"message": "Proyecto creado con éxito", "proyecto": {"nombre": nombre, "descripcion": descripcion}}), 201

        elif modulo == 'Juegos':
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')

            if not nombre or not descripcion:
                return jsonify({"error": "Debe proporcionar nombre y descripción."}), 400

            nuevo_juego = Juegos(nombre=nombre, descripcion=descripcion, id_usuario=user.id)
            db.session.add(nuevo_juego)
            db.session.commit()

            return jsonify({"message": "Juego creado con éxito", "juego": {"nombre": nombre, "descripcion": descripcion}}), 201

        else:
            return jsonify({"error": "Módulo no válido."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@catalogo_api.put('/api/catalogo/editar/')
def edit_content():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token no proporcionado."}), 400

    user = get_user_from_token(token)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    modulo = request.args.get('modulo')
    if not modulo:
        return jsonify({"error": "Debe especificar un módulo para editar contenido."}), 400

    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        return jsonify({"error": error}), 403

    permission_error = verify_edit_permission(user_privilege)
    if permission_error:
        return permission_error

    data = request.json
    try:
        if modulo == 'Materias':
            # Editar materia
            materia_id = data.get('id')
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')

            if not materia_id or not nombre or not descripcion:
                return jsonify({"error": "Debe proporcionar id, nombre y descripción."}), 400

            materia = db.session.query(Materia).filter_by(id=materia_id, id_usuario=user.id).first()

            if not materia:
                return jsonify({"error": "Materia no encontrada o no tienes acceso."}), 404

            materia.nombre = nombre
            materia.descripcion = descripcion
            db.session.commit()

            return jsonify({"message": "Materia actualizada con éxito", "materia": {"nombre": nombre, "descripcion": descripcion}}), 200

        elif modulo == 'Proyectos':
            proyecto_id = data.get('id')
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')

            if not proyecto_id or not nombre or not descripcion:
                return jsonify({"error": "Debe proporcionar id, nombre y descripción."}), 400

            proyecto = db.session.query(Proyectos).filter_by(id=proyecto_id, id_usuario=user.id).first()

            if not proyecto:
                return jsonify({"error": "Proyecto no encontrado o no tienes acceso."}), 404

            proyecto.nombre = nombre
            proyecto.descripcion = descripcion
            db.session.commit()

            return jsonify({"message": "Proyecto actualizado con éxito", "proyecto": {"nombre": nombre, "descripcion": descripcion}}), 200

        elif modulo == 'Juegos':
            # Editar juego
            juego_id = data.get('id')
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')

            if not juego_id or not nombre or not descripcion:
                return jsonify({"error": "Debe proporcionar id, nombre y descripción."}), 400

            juego = db.session.query(Juegos).filter_by(id=juego_id, id_usuario=user.id).first()

            if not juego:
                return jsonify({"error": "Juego no encontrado o no tienes acceso."}), 404

            juego.nombre = nombre
            juego.descripcion = descripcion
            db.session.commit()

            return jsonify({"message": "Juego actualizado con éxito", "juego": {"nombre": nombre, "descripcion": descripcion}}), 200

        else:
            return jsonify({"error": "Módulo no válido."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@catalogo_api.delete('/api/catalogo/delete/')
def delete_content():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token no proporcionado."}), 400

    user = get_user_from_token(token)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    modulo = request.args.get('modulo')
    if not modulo:
        return jsonify({"error": "Debe especificar un módulo para eliminar contenido."}), 400

    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        return jsonify({"error": error}), 403

    permission_error = verify_delete_permission(user_privilege)
    if permission_error:
        return permission_error

    data = request.json
    try:
        if modulo == 'Materias':
            # Eliminar materia
            materia_id = data.get('id')

            if not materia_id:
                return jsonify({"error": "Debe proporcionar el id de la materia a eliminar."}), 400

            materia = db.session.query(Materia).filter_by(id=materia_id, id_usuario=user.id).first()

            if not materia:
                return jsonify({"error": "Materia no encontrada o no tienes acceso."}), 404

            db.session.delete(materia)
            db.session.commit()

            return jsonify({"message": "Materia eliminada con éxito."}), 200

        elif modulo == 'Proyectos':
            # Eliminar proyecto
            proyecto_id = data.get('id')

            if not proyecto_id:
                return jsonify({"error": "Debe proporcionar el id del proyecto a eliminar."}), 400

            proyecto = db.session.query(Proyectos).filter_by(id=proyecto_id, id_usuario=user.id).first()

            if not proyecto:
                return jsonify({"error": "Proyecto no encontrado o no tienes acceso."}), 404

            db.session.delete(proyecto)
            db.session.commit()

            return jsonify({"message": "Proyecto eliminado con éxito."}), 200

        elif modulo == 'Juegos':
            # Eliminar juego
            juego_id = data.get('id')

            if not juego_id:
                return jsonify({"error": "Debe proporcionar el id del juego a eliminar."}), 400

            juego = db.session.query(Juegos).filter_by(id=juego_id, id_usuario=user.id).first()

            if not juego:
                return jsonify({"error": "Juego no encontrado o no tienes acceso."}), 404

            db.session.delete(juego)
            db.session.commit()

            return jsonify({"message": "Juego eliminado con éxito."}), 200

        else:
            return jsonify({"error": "Módulo no válido."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
