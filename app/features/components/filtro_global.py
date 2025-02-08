from flask import Blueprint, request, jsonify
from flask_login import login_required
from sqlalchemy import text
from db import Juegos_model, proyectos_model, materias_model, users_model, db  # Importar correctamente SQLAlchemy

search_bp = Blueprint("search", __name__)

# Función para sanitizar la entrada
def sanitizar_query(query):
    query = query.strip().lower()
    caracteres_peligrosos = ["<", ">", "'", '"', ";", "--"]
    for char in caracteres_peligrosos:
        query = query.replace(char, "")
    return query

@search_bp.route("/buscar", methods=["GET"])
@login_required  # Requiere autenticación
def buscar():
    query = request.args.get("q", "").strip()

    if not query or len(query) > 50:  # Limita la longitud para evitar abusos
        return jsonify([])

    query = sanitizar_query(query)  # Sanitiza la entrada

    # Buscar en Juegos
    juegos = Juegos_model.query.filter(Juegos_model.nombre.ilike(text(f"%{query}%"))).limit(10).all()
    juegos_result = [{"tipo": "Juego", "id": j.id, "titulo": j.nombre, "descripcion": j.descripcion} for j in juegos]

    # Buscar en Materias
    materias = materias_model.query.filter(materias_model.nombre.ilike(text(f"%{query}%"))).limit(10).all()
    materias_result = [{"tipo": "Materia", "id": m.id, "titulo": m.nombre, "descripcion": m.descripcion} for m in materias]

    # Buscar en Proyectos
    proyectos = proyectos_model.query.filter(proyectos_model.nombre.ilike(text(f"%{query}%"))).limit(10).all()
    proyectos_result = [{"tipo": "Proyecto", "id": p.id, "titulo": p.nombre, "descripcion": p.descripcion} for p in proyectos]

    # Buscar en Usuarios (solo nombre y no emails para privacidad)
    usuarios = users_model.query.filter(users_model.name.ilike(text(f"%{query}%"))).limit(10).all()
    usuarios_result = [{"tipo": "Usuario", "id": u.id, "titulo": u.name, "descripcion": "Usuario registrado"} for u in usuarios]

    # Unimos todos los resultados
    resultados = juegos_result + materias_result + proyectos_result + usuarios_result

    return jsonify(resultados)
