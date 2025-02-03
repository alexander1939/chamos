from flask import jsonify, request, session
from app.db.db import db
from app.db.users_model import User
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from app.db.materias_model import Materia
from app.db.Juegos_model import Juegos
from app.db.proyectos_model import Proyectos
from app.middleware.auth_middleware import active_tokens  

def get_user_menu():
    """Devuelve los privilegios del usuario y el contenido de los módulos a los que tiene acceso"""
    
    token = request.headers.get("Authorization")

    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Token inválido o no proporcionado"}), 401

    token = token.split(" ")[1]  

    if token not in active_tokens:
        return jsonify({"error": "Token inválido"}), 401

    user_id = active_tokens[token]["user_id"]

    # Obtener los privilegios del usuario
    user_privileges = (
        db.session.query(Privilege.name)
        .join(UserPrivilege, UserPrivilege.privilege_id == Privilege.id)
        .filter(UserPrivilege.user_id == user_id)
        .all()
    )

    privileges = [privilege.name for privilege in user_privileges]

    # Obtener el contenido de los módulos según los privilegios
    data = {}

    if "Materias" in privileges:
        materias = Materia.query.filter_by(id_usuario=user_id).all()
        data["Materias"] = [{"id": m.id, "nombre": m.nombre, "descripcion": m.descripcion} for m in materias]

    if "Juegos" in privileges:
        juegos = Juegos.query.filter_by(id_usuario=user_id).all()
        data["Juegos"] = [{"id": j.id, "nombre": j.nombre, "descripcion": j.descripcion} for j in juegos]

    if "Proyectos" in privileges:
        proyectos = Proyectos.query.filter_by(id_usuario=user_id).all()
        data["Proyectos"] = [{"id": p.id, "nombre": p.nombre, "descripcion": p.descripcion} for p in proyectos]

    return jsonify({"privilegios": privileges, "contenido": data}), 200