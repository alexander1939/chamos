from flask import Blueprint, request, jsonify
from flask_login import login_required
from db import Juegos_model, proyectos_model, materias_model, users_model  # Asegúrate de importar tus modelos

search_bp = Blueprint("search", __name__)

@search_bp.route("/buscar", methods=["GET"])
@login_required  # Opcional, si quieres restringir la búsqueda a usuarios autenticados
def buscar():
    query = request.args.get("q", "").strip().lower()
    
    if not query:
        return jsonify([])

    # Buscar en Juegos
    juegos = Juegos_model.query.filter(Juegos_model.nombre.ilike(f"%{query}%")).all()
    juegos_result = [{"tipo": "Juego", "id": j.id, "titulo": j.nombre, "descripcion": j.descripcion} for j in juegos]

    # Buscar en Materias
    materias = materias_model.query.filter(materias_model.nombre.ilike(f"%{query}%")).all()
    materias_result = [{"tipo": "Materia", "id": m.id, "titulo": m.nombre, "descripcion": m.descripcion} for m in materias]

    # Buscar en Proyectos
    proyectos = proyectos_model.query.filter(proyectos_model.nombre.ilike(f"%{query}%")).all()
    proyectos_result = [{"tipo": "Proyecto", "id": p.id, "titulo": p.nombre, "descripcion": p.descripcion} for p in proyectos]

    # Buscar en Usuarios
    usuarios = users_model.query.filter(users_model.name.ilike(f"%{query}%")).all()
    usuarios_result = [{"tipo": "Usuario", "id": u.id, "titulo": u.name, "descripcion": u.email} for u in usuarios]

    # Unimos todos los resultados
    resultados = juegos_result + materias_result + proyectos_result + usuarios_result

    return jsonify(resultados)