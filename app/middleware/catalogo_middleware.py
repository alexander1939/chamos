from app.db.db import db
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
from app.db.users_model import User
from flask import jsonify
from app.middleware.auth_middleware import active_tokens


def get_user_from_token(token):
    """Obtiene el usuario a partir del token activo."""
    if token not in active_tokens:
        return None
    user_id = active_tokens[token]["user_id"]
    return db.session.query(User).filter_by(id=user_id).first()


def has_access_to_module(user, module_name):
    """Verifica si el usuario tiene acceso al módulo solicitado."""
    privilege = db.session.query(Privilege).filter(Privilege.name == module_name).first()

    if not privilege:
        return None, "Módulo no válido"

    user_privilege = db.session.query(UserPrivilege).filter(
        UserPrivilege.user_id == user.id,
        UserPrivilege.privilege_id == privilege.id
    ).first()

    if not user_privilege or not user_privilege.can_view:
        return None, "No tienes acceso a este módulo"

    return user_privilege, None


def verify_create_permission(user_privilege):
    """Verifica si el usuario tiene permiso para crear contenido."""
    if not user_privilege.can_create:
        return jsonify({"error": "No tienes permiso para crear contenido en este módulo."}), 403
    return None


def verify_edit_permission(user_privilege):
    """Verifica si el usuario tiene permiso para editar contenido."""
    if not user_privilege.can_edit:
        return jsonify({"error": "No tienes permiso para editar contenido en este módulo."}), 403
    return None


def verify_delete_permission(user_privilege):
    """Verifica si el usuario tiene permiso para eliminar contenido."""
    if not user_privilege.can_delete:
        return jsonify({"error": "No tienes permiso para eliminar contenido en este módulo."}), 403
    return None
