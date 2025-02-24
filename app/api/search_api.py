from flask import Blueprint, request, jsonify
from app.db.users_model import User
from app.middleware.catalogo_middleware import get_user_from_token
from app.db.Materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.Juegos_model import Juegos
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
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

    query = request.args.get('query', '').strip()
    category = request.args.get('category', '').lower()
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 6, type=int)

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
    offset = (page - 1) * limit

    model_map = {
        "juegos": Juegos,
        "materias": Materia,
        "proyectos": Proyectos
    }

    # Buscar en Juegos, Materias o Proyectos
    if category in model_map:
        privilege_name = category_privileges[category]
        has_privilege = any(up.privilege.name == privilege_name for up in user_privileges)

        if not has_privilege:
            return jsonify({"error": "No tienes permisos para ver esta categoría"}), 403

        results = db.session.query(model_map[category]).filter(
            (model_map[category].nombre.ilike(f'%{query}%')) |
            (model_map[category].descripcion.ilike(f'%{query}%')),
            model_map[category].id_usuario == user.id
        ).offset(offset).limit(limit).all()

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

    # Buscar en la categoría "privilegios" (Usuarios)
    elif category == "privilegios":
        privilege_name = category_privileges[category]
        has_privilege = any(up.privilege.name == privilege_name for up in user_privileges)

        if not has_privilege:
            return jsonify({"error": "No tienes permisos para ver esta categoría"}), 403

        users = db.session.query(User).filter(
            (User.name.ilike(f"%{query}%")) |
            (User.surnames.ilike(f"%{query}%")) |
            (User.email.ilike(f"%{query}%"))
        ).offset(offset).limit(limit).all()

        for u in users:
            privileges = db.session.query(Privilege).join(UserPrivilege).filter(
                UserPrivilege.user_id == u.id
            ).all()

            results_list.append({
                "id": u.id,
                "name": u.name,
                "surnames": u.surnames,
                "email": u.email,
                "phone": u.phone,
                "privileges": [{"name": p.name} for p in privileges]
            })

    # Buscar en "todos"
    elif category == "todos":
        temp_results = []
        for up in user_privileges:
            module_name = up.privilege.name.lower()
            for key, model in model_map.items():
                if module_name == category_privileges[key].lower():
                    results = db.session.query(model).filter(
                        (model.nombre.ilike(f'%{query}%')) |
                        (model.descripcion.ilike(f'%{query}%')),
                        model.id_usuario == user.id
                    ).all()
                    for r in results:
                        temp_results.append({
                            "id": r.id,
                            "nombre": r.nombre,
                            "descripcion": getattr(r, 'descripcion', None),
                            "categoria": key.capitalize(),
                            "can_edit": up.can_edit,
                            "can_delete": up.can_delete
                        })
        
        # Aplicar paginación a los resultados combinados
        results_list = temp_results[offset:offset + limit]

    return jsonify(results_list)




# @searchApi.route('/api/buscar/<modulo>/', methods=['GET'])
# def buscar_categoria():
#     token = request.cookies.get("token")
#     if not token:
#         flash("Debes iniciar sesión para acceder a la búsqueda.", "danger")
#         return redirect(url_for('auth.login'))

#     user = get_user_from_token(token)
#     if not user:
#         flash("Usuario no encontrado.", "danger")
#         return redirect(url_for('auth.login'))

#     query = request.args.get('query', '').strip()
#     category = category.lower()

#     model_map = {
#         'materias': Materia,
#         'juegos': Juegos,
#         'proyectos': Proyectos
#     }

#     if category == "privilegios":
#         if query:
#             results = db.session.query(User).join(UserPrivilege).join(Privilege).filter(
#                 User.name.ilike(f"%{query}%") | User.surnames.ilike(f"%{query}%")
#             ).all()
#         else:
#             results = db.session.query(User).join(UserPrivilege).join(Privilege).all()
#     elif category in model_map:
#         model = model_map[category]
#         if query:
#             results = db.session.query(model).filter(
#                 model.nombre.ilike(f'%{query}%') | model.descripcion.ilike(f'%{query}%')
#             ).all()
#         else:
#             results = db.session.query(model).all()
#     else:
#         return jsonify([])

#     if category == "privilegios":
#         resultado_json = [{
#             "id": user.id,
#             "name": user.name,
#             "surnames": user.surnames,
#             "privileges": [{
#                 "name": priv.privilege.name,
#                 "can_create": priv.can_create,
#                 "can_edit": priv.can_edit,
#                 "can_delete": priv.can_delete,
#                 "can_view": priv.can_view
#             } for priv in user.user_privileges],
#             "detalles_url": url_for('auth.priv')
#         } for user in results]
#     else:
#         resultado_json = [{
#             'nombre': r.nombre,
#             'descripcion': r.descripcion,
#             'detalles_url': url_for('catalo.mostrar_detalle', modulo=category, item_id=r.id),
#             'edit_url': url_for('catalo.editar_contenido', modulo=category, item_id=r.id),
#             'delete_url': url_for('catalo.eliminar_contenido', modulo=category, item_id=r.id),
#             'can_edit': True,
#             'can_delete': True,
#             'edit_image_url': url_for('static', filename='images/edit.png'),
#             'delete_image_url': url_for('static', filename='images/delete.png')
#         } for r in results]

#     return jsonify(resultado_json)
