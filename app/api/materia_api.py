from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from app.db.db import db
from app.db.materias_model import Materia
from app.db.Juegos_model import Juegos
from app.db.proyectos_model import Proyectos
from app.middleware.auth_middleware import active_tokens,is_token_valid
from app.middleware.auth_middleware import auth_required
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
from app.db.users_model import User




materia_api = Blueprint('materias', __name__)  

# Materia API
@materia_api.get('/api/user_privileges/')
def get_user_privileges():
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        return jsonify({"error": "Token inválido o expirado, inicie sesión nuevamente"}), 401

    user_id = active_tokens[token]["user_id"]
    user = db.session.query(User).filter_by(id=user_id).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    try:
        privileges_data = []

        user_privileges = db.session.query(UserPrivilege).filter(UserPrivilege.user_id == user.id).all()
        
        for user_privilege in user_privileges:
            privilege = db.session.query(Privilege).filter(Privilege.id == user_privilege.privilege_id).first()

            if privilege:
                privileges_data.append({
                    'privilege_name': privilege.name,
                    'can_create': user_privilege.can_create,
                    'can_edit': user_privilege.can_edit,
                    'can_view': user_privilege.can_view,
                    'can_delete': user_privilege.can_delete
                })

                # Verificar si tiene privilegios para cada módulo y devolver los datos correspondientes
                if privilege.name == 'Materias' and user_privilege.can_view:
                    materias = db.session.query(Materia).filter_by(id_usuario=user.id).all()
                    privileges_data[-1]['materias'] = [{"nombre": materia.nombre, "descripcion": materia.descripcion} for materia in materias]

                elif privilege.name == 'Proyectos' and user_privilege.can_view:
                    proyectos = db.session.query(Proyectos).filter_by(id_usuario=user.id).all()
                    privileges_data[-1]['proyectos'] = [{"nombre": proyecto.nombre, "descripcion": proyecto.descripcion} for proyecto in proyectos]

                elif privilege.name == 'Juegos' and user_privilege.can_view:
                    juegos = db.session.query(Juegos).filter_by(id_usuario=user.id).all()
                    privileges_data[-1]['juegos'] = [{"nombre": juego.nombre, "descripcion": juego.descripcion} for juego in juegos]

        if not privileges_data:
            return jsonify({"message": "Este usuario no tiene privilegios asignados."}), 404

        for privilege in privileges_data:
            if 'materias' not in privilege and privilege['privilege_name'] == 'Materias':
                privilege['materias'] = "No tienes acceso a este módulo"
            if 'proyectos' not in privilege and privilege['privilege_name'] == 'Proyectos':
                privilege['proyectos'] = "No tienes acceso a este módulo"
            if 'juegos' not in privilege and privilege['privilege_name'] == 'Juegos':
                privilege['juegos'] = "No tienes acceso a este módulo"

        return jsonify({
            "user_id": user.id,
            "privileges": privileges_data
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
