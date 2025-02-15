from flask import Blueprint, request, jsonify, flash, redirect, url_for, render_template
import requests
from app.middleware.catalogo_middleware import get_user_from_token
from app.db.Materias_model import Materia
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
    if not token:
        flash("Debes iniciar sesión para acceder a la búsqueda.", "danger")
        return redirect(url_for('auth.login'))

    user = get_user_from_token(token)  
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

    if category == "todos":
        privilege_name = None
    else:
        privilege_name = category_privileges.get(category)

        if not privilege_name:
            flash("Categoría no válida.", "warning")
            return redirect(url_for('auth.index'))

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

    if privilege_name:
        can_edit = db.session.query(UserPrivilege).join(Privilege).filter(
            UserPrivilege.user_id == user.id,
            Privilege.name == privilege_name,
            UserPrivilege.can_edit == True
        ).first() is not None

        can_delete = db.session.query(UserPrivilege).join(Privilege).filter(
            UserPrivilege.user_id == user.id,
            Privilege.name == privilege_name,
            UserPrivilege.can_delete == True
        ).first() is not None
    else:
        can_edit = False
        can_delete = False

    return render_template(
        "search_results.jinja",
        resultados=resultados,
        query=query,
        category=category,
        can_edit=can_edit,
        can_delete=can_delete
    )





@search_bp.route('/buscar/<category>', methods=['GET'])
def buscar_categoria(category):
    token = request.cookies.get("token")
    if not token:
        flash("Debes iniciar sesión para acceder a la búsqueda.", "danger")
        return redirect(url_for('auth.login'))

    user = get_user_from_token(token)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))

    query = request.args.get('query', '').strip()
    category = category.lower()

    model_map = {
        'materias': Materia,
        'juegos': Juegos,
        'proyectos': Proyectos
    }

    if category == "privilegios":
        if query:
            results = db.session.query(User).join(UserPrivilege).join(Privilege).filter(
                User.name.ilike(f"%{query}%") | User.surnames.ilike(f"%{query}%")
            ).all()
        else:
            results = db.session.query(User).join(UserPrivilege).join(Privilege).all()
    elif category in model_map:
        model = model_map[category]
        if query:
            results = db.session.query(model).filter(
                model.nombre.ilike(f'%{query}%') | model.descripcion.ilike(f'%{query}%')
            ).all()
        else:
            results = db.session.query(model).all()
    else:
        return jsonify([])

    if category == "privilegios":
        resultado_json = [{
            "id": user.id,
            "name": user.name,
            "surnames": user.surnames,
            "privileges": [{
                "name": priv.privilege.name,
                "can_create": priv.can_create,
                "can_edit": priv.can_edit,
                "can_delete": priv.can_delete,
                "can_view": priv.can_view
            } for priv in user.user_privileges],
            "detalles_url": url_for('auth.priv')
        } for user in results]
    else:
        resultado_json = [{
            'nombre': r.nombre,
            'descripcion': r.descripcion,
            'detalles_url': url_for('catalo.mostrar_detalle', modulo=category, item_id=r.id),
            'edit_url': url_for('catalo.editar_contenido', modulo=category, item_id=r.id),
            'delete_url': url_for('catalo.eliminar_contenido', modulo=category, item_id=r.id),
            'can_edit': True,
            'can_delete': True,
            'edit_image_url': url_for('static', filename='images/edit.png'),
            'delete_image_url': url_for('static', filename='images/delete.png')
        } for r in results]

    return jsonify(resultado_json)
