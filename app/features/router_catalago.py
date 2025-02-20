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
@auth_required
def mostrar_contenido(user,modulo):
    return render_template("index.jinja",modulo=modulo)



@catalo_bp.get('/catalogo/<modulo>/detalle/<int:item_id>/') 
@auth_required
def mostrar_detalle(user, modulo, item_id):  # <-- Asegúrate de incluir 'user'
    return render_template("index.jinja", modulo=modulo, item_id=item_id)




@catalo_bp.route('/catalogo/agregar/<modulo>/')
@auth_required
def agregar_item(user,modulo):
    return render_template("index.jinja", modulo=modulo, agregar=True)

@catalo_bp.route('/catalogo/<modulo>/editar/<int:item_id>/', methods=['GET'])
@auth_required
def editar_contenido(user, modulo, item_id):
    return render_template("index.jinja", modulo=modulo, item_id=item_id)


