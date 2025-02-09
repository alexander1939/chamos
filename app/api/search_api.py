from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import get_current_user
from app.db.materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.Juegos_model import Juegos
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
from app.db.db import db

searchApi = Blueprint('searchApi', __name__)

@searchApi.route('/api/search', methods=['GET'])
def advanced_search():
    # Obtener usuario autenticado
    user, error_message, status_code = get_current_user()
    if error_message:
        return jsonify({"error": error_message}), status_code

    # Obtener categoría y query
    query = request.args.get('query', '')
    category = request.args.get('category', '')

    # Mapear categoría a privilegio
    category_privileges = {
        "juegos": "Juegos",
        "materias": "Materias",
        "proyectos": "Proyectos"
    }

    if category not in category_privileges:
        return jsonify({"error": "Categoría no válida"}), 400

    # Verificar si el usuario tiene el privilegio y "can_view"
    privilege_name = category_privileges[category]
    user_privilege = db.session.query(UserPrivilege).join(Privilege).filter(
        UserPrivilege.user_id == user.id,
        Privilege.name == privilege_name,
        UserPrivilege.can_view == True
    ).first()

    if not user_privilege:
        return jsonify({"error": "No tienes permisos para ver esta categoría"}), 403

    # Obtener resultados de la categoría
    model_map = {
        "juegos": Juegos,
        "materias": Materia,
        "proyectos": Proyectos
    }
    
    results = db.session.query(model_map[category]).filter(
        model_map[category].nombre.ilike(f'%{query}%'),
        model_map[category].id_usuario == user.id  # Solo muestra datos del usuario autenticado
    ).all()

    return jsonify([{
        "id": r.id,
        "nombre": r.nombre,
        "descripcion": getattr(r, 'descripcion', None)
    } for r in results])
