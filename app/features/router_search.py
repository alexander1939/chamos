from flask import Blueprint, request, jsonify, flash, redirect, url_for, render_template
import requests
from app.middleware.catalogo_middleware import get_user_from_token
from app.db.materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.Juegos_model import Juegos
from app.db.UserPrivilege_model import UserPrivilege
from app.db.Privilege_model import Privilege
from app.db.users_model import User
from app.middleware.auth_middleware import get_current_user
from app.db.db import db

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/buscar', methods=['GET'])
def buscar():
    token = request.cookies.get("token")
    print("Token recibido router: ", token)
    if not token:
        flash("Debes iniciar sesión para acceder a la búsqueda.", "danger")
        return redirect(url_for('auth.login'))

    user = get_user_from_token(token)  
    print("Usuario obtenido desde el token: ", user)

    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))

    query = request.args.get('query', '').strip()
    category = request.args.get('category', '').strip()

    if not query or not category:
        flash("Debes ingresar un término de búsqueda y seleccionar una categoría.", "warning")
        return redirect(url_for('auth.index'))

    category_privileges = {
        "juegos": "Juegos",
        "materias": "Materias",
        "proyectos": "Proyectos",
        "privilegios": "Gestionar Privilegios"
    }

    if category not in category_privileges:
        flash("Categoría no válida.", "warning")
        return redirect(url_for('auth.index'))

    privilege_name = category_privileges[category]
    user_privilege = db.session.query(UserPrivilege).join(Privilege).filter(
        UserPrivilege.user_id == user.id, 
        Privilege.name == privilege_name,
        UserPrivilege.can_view == True
    ).first()

    if not user_privilege:
        flash("No tienes permisos para ver esta categoría.", "danger")
        return redirect(url_for('auth.index'))

    api_url = request.host_url + "api/search"
    params = {'query': query, 'category': category}

    try:
        cookies = {'token': token}
        response = requests.get(api_url, params=params, cookies=cookies)
        response_data = response.json()

        if response.status_code == 200:
            resultados = response_data
        else:
            flash(response_data.get("error", "Error en la búsqueda."), "danger")
            return redirect(url_for('auth.index'))

    except requests.exceptions.RequestException:
        flash("Error al conectar con el servidor.", "danger")
        return redirect(url_for('auth.index'))

    return render_template("search_results.jinja", resultados=resultados, query=query, category=category)

    
@search_bp.route('/categorias', methods=['GET'])
def obtener_categorias():
    token = request.cookies.get("token")

    if not token:
        return {}, 403  

    user, error_message, status_code = get_current_user()
    if error_message:
        return {}, 403

    privilegios_usuario = db.session.query(UserPrivilege).join(Privilege).filter(
        UserPrivilege.user_id == user.id,
        UserPrivilege.can_view == True
    ).all()

    categorias_disponibles = {p.privilege.name.split()[-1].lower(): p.privilege.name.split()[-1] for p in privilegios_usuario}

    return categorias_disponibles, 200
