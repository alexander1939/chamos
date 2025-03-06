from flask import Blueprint, request, jsonify
from app.db.Materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.Juegos_model import Juegos
from app.middleware.catalogo_middleware import get_user_from_token, has_access_to_module, verify_create_permission, verify_edit_permission, verify_delete_permission
from app.db.db import db
from app.db.UserPrivilege_model import UserPrivilege
from app.db.users_model import User


catalogo_api = Blueprint('catalogo', __name__)


@catalogo_api.get('/api/validate_token')
def validate_token():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token no proporcionado."}), 401

    user = get_user_from_token(token)
    if not user:
        return jsonify({"error": "Token inválido o expirado."}), 401

    return jsonify({"message": "Token válido"}), 200



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
        response_data = {
            "can_create": user_privilege.can_create,
            "can_edit": user_privilege.can_edit,
            "can_view": user_privilege.can_view,
            "can_delete": user_privilege.can_delete,
        }

        if modulo == 'Materias':
            response_data["materias"] = [
                {"id": materia.id, "nombre": materia.nombre, "descripcion": materia.descripcion}
                for materia in db.session.query(Materia).filter_by(id_usuario=user.id).all()
            ]
        elif modulo == 'Proyectos':
            response_data["proyectos"] = [
                {"id": proyecto.id, "nombre": proyecto.nombre, "descripcion": proyecto.descripcion}
                for proyecto in db.session.query(Proyectos).filter_by(id_usuario=user.id).all()
            ]
        elif modulo == 'Juegos':
            response_data["juegos"] = [
                {"id": juego.id, "nombre": juego.nombre, "descripcion": juego.descripcion}
                for juego in db.session.query(Juegos).filter_by(id_usuario=user.id).all()
            ]
        else:
            return jsonify({"error": "Módulo no válido."}), 400

        return jsonify(response_data)

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

    # Obtener 'modulo' e 'id' de los parámetros de la URL (query parameters)
    modulo = request.args.get('modulo')
    item_id = request.args.get('id')

    if not modulo:
        return jsonify({"error": "Debe especificar un módulo."}), 400
    if not item_id:
        return jsonify({"error": "Debe especificar un ID."}), 400

    # Convertir item_id a entero (si es necesario)
    item_id = int(item_id)

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

        elif modulo == 'Gestionar Privilegios':
            user_priv = db.session.query(UserPrivilege).join(User).filter(User.id == item_id).first()
            if not user_priv:
                return jsonify({"error": "Usuario no encontrado o sin privilegios."}), 404

            can_create = user_priv.can_create if user_priv else False
            can_edit = user_priv.can_edit if user_priv else False
            can_view = user_priv.can_view if user_priv else False
            can_delete = user_priv.can_delete if user_priv else False

            return jsonify({
                "modulo": "Gestionar Privilegios",
                "can_view": can_view,
                "detalle": {
                    "id": user_priv.user.id,
                    "nombre": user_priv.user.name,
                    "descripcion": f"Email: {user_priv.user.email}, Teléfono: {user_priv.user.phone}",
                    "privilegio": user_priv.privilege.name,
                    "puede_crear": can_create,
                    "puede_editar": can_edit,
                    "puede_ver": can_view,
                    "puede_eliminar": can_delete
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

@catalogo_api.get('/api/catalogo/carrusel/')
def get_carrusel():
    token = request.cookies.get("token")
    if not token:
        return jsonify({"error": "Token no proporcionado."}), 400

    user = get_user_from_token(token)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    # Módulos posibles
    modules = {
        "Materias": "/static/images/carrusel/materias1.jpg",
        "Juegos": "/static/images/carrusel/juegos.jpg",
        "Proyectos": "/static/images/carrusel/proyectos.jpg"
    }
    
    allowed_modules = []

    # Verifica los privilegios del usuario para cada módulo
    for module, image_url in modules.items():
        user_privilege, error = has_access_to_module(user, module)
        if user_privilege and error is None:
            allowed_modules.append({"module": module, "image": image_url})

    # Si el usuario no tiene acceso a ningún módulo, devuelve un error
    if not allowed_modules:
        return jsonify({"error": "No tienes acceso a ningún módulo."}), 403

    return jsonify({
        "carrusel": allowed_modules  # Devuelve los módulos permitidos y sus respectivas imágenes
    })
