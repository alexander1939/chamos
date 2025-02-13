from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.api.catalago_api import get_user_catalog,add_new_content,get_catalogo_detalle    # Importamos la función directamente
from app.middleware.auth_middleware import active_tokens
from app.middleware.catalogo_middleware import get_user_from_token, has_access_to_module, verify_create_permission, verify_edit_permission, verify_delete_permission
import requests  # Asegúrate de importar requests
from app.db.Materias_model import Materia
from app.db.Juegos_model import Juegos
from app.db.proyectos_model import Proyectos
from app.db.UserPrivilege_model import UserPrivilege






catalo_bp = Blueprint('catalo', __name__)

@catalo_bp.route('/catalogo/<modulo>/')
def mostrar_contenido(modulo):
    return render_template("models/index.jinja", modulo=modulo)



@catalo_bp.get('/catalogo/<modulo>/detalle/<int:item_id>/')
def mostrar_detalle(modulo, item_id):
    token = request.cookies.get("token")
    
    if not token or token not in active_tokens:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('auth.login'))

    user = get_user_from_token(token)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))

    # Verificar privilegios de usuario
    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        flash(error, "warning")
        return redirect(url_for('auth.index'))

    # Llamada a la API para obtener el detalle
    api_url = f"http://localhost:5000/api/catalogo/detalle/?modulo={modulo}"
    response = requests.get(api_url, json={'id': item_id}, cookies=request.cookies)

    if response.status_code == 200:
        response_json = response.json()
        can_view = response_json.get("can_view", False)

        if not can_view:
            flash(f"No tienes permiso para ver este {modulo.lower()}.", "warning")
            return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))

        detalle = response_json.get("detalle", {})
        return render_template("models/detail_categoria.jinja", detalle=detalle, modulo=modulo)
    
    flash(response.json().get("error", "Error al obtener detalles del contenido"), "danger")
    return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))





@catalo_bp.route('/catalogo/<modulo>/agregar/', methods=['GET', 'POST'])
def agregar_contenido(modulo):
    token = request.cookies.get("token")
    
    if not token or token not in active_tokens:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('auth.login'))

    user = get_user_from_token(token)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))

    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        flash(error, "warning")
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        can_create = user_privilege.can_create
        if not can_create:
            flash(f"No tienes permiso para agregar {modulo.lower()}.", "warning")
            return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))

        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        if not nombre or not descripcion:
            flash("Debe proporcionar nombre y descripción.", "warning")
            return redirect(url_for('catalo.agregar_contenido', modulo=modulo))

        data = {'nombre': nombre, 'descripcion': descripcion}
        api_url = f"http://localhost:5000/api/catalogo/agregar/?modulo={modulo}"

        response = requests.post(api_url, json=data, cookies=request.cookies)

        if response.status_code == 201:
            flash(f"{modulo} agregado correctamente.", "success")
            return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))
        else:
            error_message = response.json().get('error', 'Error desconocido')
            flash(f"Error al agregar {modulo}: {error_message}", "danger")
            return redirect(url_for('catalo.agregar_contenido', modulo=modulo))

    context = {
        'form_title': f'Agregar Nuevo {modulo}',
        'action_url': url_for('catalo.agregar_contenido', modulo=modulo),
        'input_title': f'Nombre de {modulo}',
        'desc_title': f'Descripción de {modulo}',
        'button_text': f'Agregar {modulo}',
        'item_name': '',
        'item_description': '',
        'modulo': modulo 
    }

    return render_template("models/add_categoria.jinja", **context)


@catalo_bp.route('/catalogo/<modulo>/editar/<int:item_id>/', methods=['GET', 'POST'])
def editar_contenido(modulo, item_id):
    token = request.cookies.get("token")
    
    if not token or token not in active_tokens:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('auth.login'))

    user = get_user_from_token(token)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))

    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        flash(error, "warning")
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        can_edit = user_privilege.can_edit
        if not can_edit:
            flash(f"No tienes permiso para editar {modulo.lower()}.", "warning")
            return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))

        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        if not nombre or not descripcion:
            flash("Debe proporcionar nombre y descripción.", "warning")
            return redirect(url_for('catalo.editar_contenido', modulo=modulo, item_id=item_id))

        data = {'id': item_id, 'nombre': nombre, 'descripcion': descripcion}
        api_url = f"http://localhost:5000/api/catalogo/editar/?modulo={modulo}"

        response = requests.put(api_url, json=data, cookies=request.cookies)

        if response.status_code == 200:
            flash(f"{modulo} editado correctamente.", "success")
            return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))
        else:
            error_message = response.json().get('error', 'Error desconocido')
            flash(f"Error al editar {modulo}: {error_message}", "danger")
            return redirect(url_for('catalo.editar_contenido', modulo=modulo, item_id=item_id))

    if modulo == 'Materias':
        item = Materia.query.filter_by(id=item_id, id_usuario=user.id).first()
    elif modulo == 'Proyectos':
        item = Proyectos.query.filter_by(id=item_id, id_usuario=user.id).first()
    elif modulo == 'Juegos':
        item = Juegos.query.filter_by(id=item_id, id_usuario=user.id).first()
    else:
        flash("Módulo no válido.", "danger")
        return redirect(url_for('auth.index'))

    if not item:
        flash(f"{modulo} no encontrado o no tienes acceso.", "danger")
        return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))

    context = {
        'form_title': f'Editar {modulo}',
        'action_url': url_for('catalo.editar_contenido', modulo=modulo, item_id=item_id),
        'input_title': f'Nombre de {modulo}',
        'desc_title': f'Descripción de {modulo}',
        'button_text': f'Editar {modulo}',
        'item_name': item.nombre,
        'item_description': item.descripcion,
        'modulo': modulo 
    }

    return render_template("models/edit_categoria.jinja", **context)


@catalo_bp.post('/catalogo/<modulo>/eliminar/<int:item_id>/')
def eliminar_contenido(modulo, item_id):
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('auth.login'))

    user = get_user_from_token(token)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))

    user_privilege, error = has_access_to_module(user, modulo)
    if error:
        flash(error, "warning")
        return redirect(url_for('auth.index'))

    if not user_privilege.can_delete:
        flash(f"No tienes permiso para eliminar {modulo.lower()}.", "warning")
        return redirect(url_for('auth.index'))

    api_url = f"http://localhost:5000/api/catalogo/delete/?modulo={modulo}"
    data = {'id': item_id}

    response = requests.delete(api_url, json=data, cookies=request.cookies)

    if response.status_code == 200:
        flash(f"{modulo} eliminado correctamente.", "success")
    else:
        error_message = response.json().get('error', 'Error desconocido')
        flash(f"Error al eliminar {modulo}: {error_message}", "danger")

    return redirect(url_for('catalo.mostrar_contenido', modulo=modulo))

