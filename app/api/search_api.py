from flask import Blueprint, request, jsonify
from app.middleware.catalogo_middleware import get_user_from_token, has_access_to_module, verify_create_permission, verify_edit_permission, verify_delete_permission
from app.db.Materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.Juegos_model import Juegos
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
from app.db.users_model import User
from app.db.db import db

searchApi = Blueprint('searchApi', __name__)

@searchApi.get('/api/search')
def advanced_search():
    token = request.cookies.get("token")
    print("Token recibido api: ", token)

    if not token:
        return jsonify({"error": "Token no proporcionado."}), 400

    user = get_user_from_token(token)
    if not user:
        return jsonify({"error": "Usuario no encontrado."}), 404

    query = request.args.get('query', '')
    category = request.args.get('category', '')

    category_privileges = {
        "juegos": "Juegos",
        "materias": "Materias",
        "proyectos": "Proyectos",
        "privilegios": "Gestionar Privilegios",
        "todos": "Todos"
    }

    if category not in category_privileges:
        return jsonify({"error": "Categoría no válida"}), 400

    user_privileges = db.session.query(UserPrivilege).join(Privilege).filter(
        UserPrivilege.user_id == user.id,
        UserPrivilege.can_view == True
    ).all()

    if not user_privileges:
        return jsonify({"error": "No tienes permisos en ningún módulo"}), 403

    results_list = []

    if category in category_privileges and category != "todos":
        privilege_name = category_privileges[category]
        has_privilege = any(up.privilege.name == privilege_name for up in user_privileges)

        if not has_privilege:
            return jsonify({"error": "No tienes permisos para ver esta categoría"}), 403

        if category == "privilegios":
            results = db.session.query(UserPrivilege).join(User).join(Privilege).filter(
                (User.name.ilike(f'%{query}%')) |
                (User.email.ilike(f'%{query}%')) |
                (User.phone.ilike(f'%{query}%')) |
                (Privilege.name.ilike(f'%{query}%'))
            ).all()

            user_privileges_data = {}
            for up in results:
                user_id = up.user_id
                if user_id not in user_privileges_data:
                    user_privileges_data[user_id] = {
                        "nombre": up.user.name,
                        "descripcion": f"Email: {up.user.email}, Teléfono: {up.user.phone}",
                    }
                user_privileges_data[user_id].setdefault("privilegios", []).append(up.privilege.name)

            results_list = list(user_privileges_data.values())

            for user in results_list:
                privilegios = user.pop("privilegios", [])
                for privilegio in privilegios:
                    if privilegio == "Gestionar Privilegios":
                        privilegio = "privilegios"
                    user[privilegio] = privilegio

        else:
            model_map = {
                "juegos": Juegos,
                "materias": Materia,
                "proyectos": Proyectos
            }

            results = db.session.query(model_map[category]).filter(
                (model_map[category].nombre.ilike(f'%{query}%')) |
                (model_map[category].descripcion.ilike(f'%{query}%')),
                model_map[category].id_usuario == user.id
            ).all()

            results_list = [{
                "nombre": r.nombre,
                "descripcion": getattr(r, 'descripcion', None)
            } for r in results]

    elif category == "todos":
        model_map = {
            "juegos": Juegos,
            "materias": Materia,
            "proyectos": Proyectos
        }

        for up in user_privileges:
            module_name = up.privilege.name.lower()

            for key, model in model_map.items():
                if module_name == category_privileges[key].lower():
                    results = db.session.query(model).filter(
                        (model.nombre.ilike(f'%{query}%')) |
                        (model.descripcion.ilike(f'%{query}%'))).all()


                    results_list.extend([{
                        "categoria": key,
                        "nombre": r.nombre,
                        "descripcion": getattr(r, 'descripcion', None)
                    } for r in results])

        if any(up.privilege.name == "Gestionar Privilegios" for up in user_privileges):
            privilege_results = db.session.query(UserPrivilege).join(User).join(Privilege).filter(
                (User.name.ilike(f'%{query}%')) |
                (User.email.ilike(f'%{query}%')) |
                (User.phone.ilike(f'%{query}%')) |
                (Privilege.name.ilike(f'%{query}%'))
            ).all()

            user_privileges_data = {}
            for up in privilege_results:
                user_id = up.user_id
                if user_id not in user_privileges_data:
                    user_privileges_data[user_id] = {
                        "categoria": "privilegios",
                        "nombre": up.user.name,
                        "email":up.user.email,
                        "Teléfono":up.user.phone
                    }
                user_privileges_data[user_id].setdefault("privilegios", []).append(up.privilege.name)

            result_list = list(user_privileges_data.values())

            for user in result_list:
                privilegios = user.pop("privilegios", [])
                for privilegio in privilegios:
                    if privilegio == "Gestionar Privilegios":
                        privilegio = "privilegios"
                    user[privilegio] = privilegio

            results_list.extend(result_list)

    if not results_list:
        return jsonify({"mensaje": "No se encontraron resultados"}), 200

    return jsonify(results_list)
