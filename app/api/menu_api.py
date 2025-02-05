from flask import Blueprint, request, render_template,jsonify
from app.db.db import db
from app.db.users_model import User
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Materias_model import Materia
from app.db.Juegos_model import Juegos
from app.db.proyectos_model import Proyectos
from app.middleware.auth_middleware import active_tokens


menu = Blueprint('menu', __name__)

@menu.route('/api/menu', methods=['GET'])
def get_user_menu():
    """Devuelve los privilegios del usuario y el contenido de los módulos a los que tiene acceso"""

    # 🔹 Obtener el token de la cookie en lugar del header
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        return jsonify({"error": "Token inválido o no proporcionado"}), 401

    user_id = active_tokens[token]["user_id"]

    # Obtener los datos del usuario
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

    # Obtener los privilegios del usuario
    user_privileges = (
        db.session.query(Privilege.name)
        .join(UserPrivilege, UserPrivilege.privilege_id == Privilege.id)
        .filter(UserPrivilege.user_id == user_id)
        .all()
    )

    privileges = [privilege.name for privilege in user_privileges]

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

    return jsonify({"usuario": user_data, "privilegios": privileges, "contenido": data}), 200
