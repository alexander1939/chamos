from flask import Blueprint, jsonify,request
from sqlalchemy.orm import joinedload
from app.db.db import db
from app.db.users_model import User
from app.db.Privilege_model import Privilege
from app.middleware.user_access_middleware import user_or_admin_required,admin_required
from app.db.UserPrivilege_model import UserPrivilege


usersApi = Blueprint('usersApi', __name__)

@usersApi.route('/api/users/', methods=['GET'])
@user_or_admin_required
def get_users(current_user):
    """Si el usuario es admin, obtiene todos los usuarios con rol 'Usuario'. Si es usuario, obtiene solo su información, incluyendo privilegios y permisos."""

    if current_user.role.name == "Admin":
        users = User.query.options(
            joinedload(User.role),
            joinedload(User.user_privileges).joinedload(UserPrivilege.privilege)  
        ).filter(User.role.has(name="Usuario")).all()
    else:
        users = [current_user]

    users_data = [
        {
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "surnames": u.surnames,
            "phone": u.phone,
            "role": u.role.name,
            "pregunta1": u.pregunta1,
            "respuesta1": u.respuesta1,
            "pregunta2": u.pregunta2,
            "respuesta2": u.respuesta2,
            "privileges": [
                {
                    "id": p.privilege.id,
                    "name": p.privilege.name,
                    "description": p.privilege.description,
                    "can_create": p.can_create,
                    "can_edit": p.can_edit,
                    "can_view": p.can_view,
                    "can_delete": p.can_delete
                } for p in u.user_privileges
            ]
        } for u in users
    ]

    return jsonify(users_data), 200

@usersApi.route('/api/users/<int:user_id>/privileges', methods=['PUT'])
@admin_required 
def update_user_privileges(user_id):
    """Permite a un administrador modificar los privilegios y permisos (can_create, can_edit, can_view, can_delete) de un usuario."""
    
    data = request.get_json()
    new_privileges = data.get("privileges")

    if not isinstance(new_privileges, list):
        return jsonify({"error": "Se requiere una lista de privilegios con permisos"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Eliminar privilegios actuales del usuario
    UserPrivilege.query.filter_by(user_id=user_id).delete()

    # Asignar nuevos privilegios con los permisos definidos
    for privilege_data in new_privileges:
        privilege_id = privilege_data.get("id")
        can_create = privilege_data.get("can_create", False)
        can_edit = privilege_data.get("can_edit", False)
        can_view = privilege_data.get("can_view", False)
        can_delete = privilege_data.get("can_delete", False)

        privilege = Privilege.query.get(privilege_id)
        if privilege:
            new_user_privilege = UserPrivilege(
                user_id=user_id,
                privilege_id=privilege_id,
                can_create=can_create,
                can_edit=can_edit,
                can_view=can_view,
                can_delete=can_delete
            )
            db.session.add(new_user_privilege)

    db.session.commit()
    return jsonify({"message": "Privilegios y permisos actualizados correctamente"}), 200