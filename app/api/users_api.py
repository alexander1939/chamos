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
    """Si el usuario es admin, obtiene todos los usuarios con rol 'Usuario'. Si es usuario, obtiene solo su información, incluyendo privilegios."""

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
            "privileges": [
                {
                    "id": p.privilege.id,
                    "name": p.privilege.name,
                    "description": p.privilege.description
                } for p in u.user_privileges
            ]
        } for u in users
    ]

    return jsonify(users_data), 200

@usersApi.route('/api/users/<int:user_id>/privileges', methods=['PUT'])
@admin_required 
def update_user_privileges(user_id):
    """Permite a un administrador modificar los privilegios de un usuario."""
    
    data = request.get_json()
    new_privileges = data.get("privileges")

    if not isinstance(new_privileges, list):
        return jsonify({"error": "Se requiere una lista de IDs de privilegios"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    UserPrivilege.query.filter_by(user_id=user_id).delete()

    for privilege_id in new_privileges:
        privilege = Privilege.query.get(privilege_id)
        if privilege:
            db.session.add(UserPrivilege(user_id=user_id, privilege_id=privilege_id))

    db.session.commit()
    return jsonify({"message": "Privilegios actualizados correctamente"}), 200