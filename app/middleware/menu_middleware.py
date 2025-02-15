from functools import wraps
from flask import request, jsonify
from app.db.db import db
from app.db.users_model import User
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from app.middleware.auth_middleware import active_tokens
from sqlalchemy.orm import joinedload

def get_current_user():
    """Obtiene el usuario autenticado a partir del token."""
    token = request.cookies.get("token")
    
    if not token or token not in active_tokens:
        return None, jsonify({"error": "Token inválido o no proporcionado"}), 401
    
    user_id = active_tokens[token]["user_id"]
    user = db.session.query(User).filter_by(id=user_id).first()
    
    if not user:
        return None, jsonify({"error": "Usuario no encontrado"}), 404
    
    return user, None, None

def menu_required(f):
    """Middleware para validar el usuario y obtener sus privilegios."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user, error_response, status_code = get_current_user()
        if error_response:
            return error_response, status_code

        user_privileges = (
            db.session.query(UserPrivilege)
            .join(Privilege, UserPrivilege.privilege_id == Privilege.id)
            .filter(UserPrivilege.user_id == user.id)
            .all()
        )

        privileges = {
            priv.privilege.name: {
                "can_create": getattr(priv, "can_create", False),
                "can_view": getattr(priv, "can_view", False)
            }
            for priv in user_privileges
        }

        return f(user, privileges, *args, **kwargs)
    
    return decorated_function

def get_privilege_content(user, privileges):
    """Genera el contenido basado en los privilegios del usuario."""
    menu_items = []
    
    for privilege_name, permission in privileges.items():
        contenido = []

        if privilege_name == "Gestionar Privilegios":
            users = User.query.options(joinedload(User.role)).filter(User.role.has(name="Usuario")).all()
            contenido = [{"id": u.id, "name": u.name, "email": u.email} for u in users]

        elif privilege_name == "Materias":
            from app.db.Materias_model import Materia
            materias = Materia.query.filter_by(id_usuario=user.id).all()
            contenido = [{"id": m.id, "nombre": m.nombre, "descripcion": m.descripcion} for m in materias]

        elif privilege_name == "Juegos":
            from app.db.Juegos_model import Juegos
            juegos = Juegos.query.filter_by(id_usuario=user.id).all()
            contenido = [{"id": j.id, "nombre": j.nombre, "descripcion": j.descripcion} for j in juegos]

        elif privilege_name == "Proyectos":
            from app.db.proyectos_model import Proyectos
            proyectos = Proyectos.query.filter_by(id_usuario=user.id).all()
            contenido = [{"id": p.id, "nombre": p.nombre, "descripcion": p.descripcion} for p in proyectos]

        menu_items.append({
            "nombre": privilege_name,
            "contenido": contenido,
            "can_create": permission["can_create"],
            "can_view": permission["can_view"]
        })
    
    return menu_items