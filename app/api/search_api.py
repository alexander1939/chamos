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

        model_map = {
            "juegos": Juegos,
            "materias": Materia,
            "proyectos": Proyectos
        }

        results = db.session.query(model_map[category]).filter(
            (model_map[category].nombre.ilike(f'%{query}%')) |
            (model_map[category].descripcion.ilike(f'%{query}%'))
        ).all()

        for r in results:
            user_privilege = db.session.query(UserPrivilege).join(Privilege).filter(
                UserPrivilege.user_id == user.id,
                Privilege.name == privilege_name
            ).first()

            results_list.append({
                "id": r.id,
                "nombre": r.nombre,
                "descripcion": getattr(r, 'descripcion', None),
                "categoria": category,
                "can_edit": user_privilege.can_edit if user_privilege else False,
                "can_delete": user_privilege.can_delete if user_privilege else False
            })

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
                        (model.descripcion.ilike(f'%{query}%'))
                    ).all()

                    for r in results:
                        results_list.append({
                            "id": r.id,
                            "nombre": r.nombre,
                            "descripcion": getattr(r, 'descripcion', None),
                            "categoria": key.capitalize(), 
                            "can_edit": up.can_edit,
                            "can_delete": up.can_delete
                        })

    if not results_list:
        return jsonify([]), 200

    return jsonify(results_list)
