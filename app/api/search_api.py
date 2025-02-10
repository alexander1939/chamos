from flask import Blueprint, request, jsonify
from app.middleware.catalogo_middleware import get_user_from_token, has_access_to_module, verify_create_permission, verify_edit_permission, verify_delete_permission
from app.db.materias_model import Materia
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
        "privilegios": "Gestionar Privilegios"
    }

    if category not in category_privileges:
        return jsonify({"error": "Categoría no válida"}), 400

    privilege_name = category_privileges[category]
    user_privilege = db.session.query(UserPrivilege).join(Privilege).filter(
        UserPrivilege.user_id == user.id,
        Privilege.name == privilege_name,
        UserPrivilege.can_view == True
    ).first()

    if not user_privilege:
        return jsonify({"error": "No tienes permisos para ver esta categoría"}), 403

    # Obtener resultados de la categoría
    if category in ["juegos", "materias", "proyectos"]:
        model_map = {
            "juegos": Juegos,
            "materias": Materia,
            "proyectos": Proyectos
        }

        results = db.session.query(model_map[category]).filter(
            model_map[category].nombre.ilike(f'%{query}%'),
            model_map[category].id_usuario == user.id  
        ).all()

        return jsonify([{
            "nombre": r.nombre,
            "descripcion": getattr(r, 'descripcion', None)
        } for r in results])

    elif category == "privilegios":
        results = db.session.query(UserPrivilege).join(User).join(Privilege).all()

        user_privileges = {}

        for up in results:
            user_id = up.user_id
            if user_id not in user_privileges:
                user_privileges[user_id] = {
                    "nombre": up.user.name,
                    "descripcion": f"Email: {up.user.email}, Teléfono: {up.user.phone}",
                }

            user_privileges[user_id].setdefault("privilegios", []).append(up.privilege.name)

        result_list = list(user_privileges.values())

        # Ahora aseguramos que "Gestionar Privilegios" se convierte en "privilegios"
        for user in result_list:
            privilegios = user.pop("privilegios", [])
            for privilegio in privilegios:
                if privilegio == "Gestionar Privilegios":
                    privilegio = "privilegios"  # Cambiamos el nombre del privilegio
                user[privilegio] = privilegio  # Asignamos el privilegio con el nuevo nombre

        return jsonify(result_list)
