from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from app import db
from app.api.catalago_api import get_user_catalog,add_new_content,get_catalogo_detalle    # Importamos la función directamente
from app.middleware.auth_middleware import active_tokens, auth_required
from app.middleware.catalogo_middleware import get_user_from_token, has_access_to_module, verify_create_permission, verify_edit_permission, verify_delete_permission
import requests  # Asegúrate de importar requests
from app.db.Materias_model import Materia
from app.db.Juegos_model import Juegos
from app.db.proyectos_model import Proyectos
from app.db.UserPrivilege_model import UserPrivilege
from app.middleware.auth_middleware import  auth_required
from flask import current_app








catalo_bp = Blueprint('catalo', __name__)

@catalo_bp.route('/catalogo/<modulo>/')
def mostrar_contenido(modulo):
    return render_template("index.jinja",modulo=modulo)



@catalo_bp.get('/catalogo/<modulo>/detalle/<int:item_id>/') 
@auth_required
def mostrar_detalle(user, modulo, item_id):  # <-- Asegúrate de incluir 'user'
    user_privilege, error = has_access_to_module(user, modulo)  # <-- Pasar user aquí
    if error:
        flash(error, "warning")
        return redirect(url_for('auth.index'))

    return render_template("index.jinja", modulo=modulo, item_id=item_id)





@catalo_bp.route('/catalogo/<modulo>/agregar/', methods=['GET'])
@auth_required
def agregar_contenido(user, modulo):
    return render_template("index.jinja", modulo=modulo)


@catalo_bp.route('/catalogo/<modulo>/editar/<int:item_id>/', methods=['GET'])
@auth_required
def editar_contenido(user, modulo, item_id):
    return render_template("index.jinja", modulo=modulo, item_id=item_id)



@catalo_bp.route('/catalogo/<modulo>/eliminar/<int:item_id>/', methods=['POST'])
@auth_required
def eliminar_contenido(user, modulo, item_id):
    # Verificar permisos del usuario
    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        flash(error, "warning")
        return redirect(url_for('auth.index'))

    # Verificar si el usuario tiene permiso para eliminar
    if not user_privilege.can_delete:
        flash(f"No tienes permiso para eliminar {modulo.lower()}.", "warning")
        return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))

    # Renderizar el template de confirmación
    context = {
        'modulo': modulo,
        'item_id': item_id,
        'action_url': url_for('catalo.eliminar_contenido', modulo=modulo, item_id=item_id)
    }
    return render_template("index.jinja", **context)