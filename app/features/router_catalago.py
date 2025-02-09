from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.api.catalago_api import get_user_catalog,add_new_content  # Importamos la función directamente
from app.middleware.auth_middleware import active_tokens
from app.middleware.catalogo_middleware import get_user_from_token, has_access_to_module, verify_create_permission, verify_edit_permission, verify_delete_permission
import requests  # Asegúrate de importar requests
from app.db.materias_model import Materia



catalo_bp = Blueprint('catalo', __name__)

@catalo_bp.route('/materias/')
def mostrar_materias():
    token = request.cookies.get("token")

    if not token or token not in active_tokens:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('auth.login'))

    # 🔹 Pasamos el módulo correcto como parámetro
    request.args = {'modulo': 'Materias'}  

    # 🔹 Llamar a la API de catálogo y recibir ambos valores (Response, status_code)
    response = get_user_catalog()  # Llamamos a la función de catálogo
    
    if isinstance(response, tuple):  # Si recibimos una tupla (Response, status_code)
        response, status_code = response  # Desempaquetamos correctamente
    else:
        status_code = response.status_code  # Si solo recibimos un Response, tomamos el código de estado

    response_json = response.get_json() if hasattr(response, 'get_json') else response

    # 🔹 Verificamos el código de estado
    if status_code == 200:
        can_view = response_json.get("can_view", False)  # Verificamos si tiene permiso para ver
        can_create = response_json.get("can_create", False)  # Verificamos si tiene permiso para crear
        can_edit = response_json.get("can_edit", False)  # Verificamos si tiene permiso para editar
        can_delete = response_json.get("can_delete", False)  # Verificamos si tiene permiso para eliminar

        if not can_view:  # Si no tiene permiso para ver
            flash("No tienes acceso a este módulo.", "warning")
            return redirect(url_for('auth.index'))  # Redirigir si no tiene permiso para ver

        # Si tiene permiso para ver, mostramos las materias
        materias = response_json.get("materias", [])
    elif status_code == 403:  # Usuario sin privilegios
        flash("No tienes acceso a este módulo.", "warning")
        return redirect(url_for('auth.index'))  # Redirigir si no tiene acceso
    else:
        flash(response_json.get("error", "Error al obtener materias"), "danger")
        materias = []

    return render_template("materias/index.jinja", materias=materias, can_create=can_create, can_edit=can_edit, can_delete=can_delete)




@catalo_bp.route('/materias/agregar/', methods=['GET', 'POST'])
def agregar_materia():
    token = request.cookies.get("token")
    
    # Verificar si el token está presente
    if not token or token not in active_tokens:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('auth.login'))  # Redirige al login si no tiene sesión activa

    # Obtener el usuario desde el token
    user = get_user_from_token(token)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))  # Redirige al login si el usuario no existe

    # Verificamos el acceso al módulo de 'Materias'
    modulo = 'Materias'
    user_privilege, error = has_access_to_module(user, modulo)
    if error:  # Si no tiene acceso
        flash(error, "warning")
        return redirect(url_for('auth.index'))  # Redirige al index si no tiene acceso

    # Si el método es POST, procesamos el formulario
    if request.method == 'POST':
        can_create = user_privilege.can_create  # Verificamos si el usuario tiene permiso para crear
        if not can_create:
            flash("No tienes permiso para crear una materia.", "warning")
            return redirect(url_for('auth.index'))  # Redirige al index si no tiene permiso de creación

        # Procesamos los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        if not nombre or not descripcion:
            flash("Debe proporcionar nombre y descripción para la nueva materia.", "warning")
            return redirect(url_for('catalo.agregar_materia'))  # Redirige si falta algún dato

        # Llamamos a la función de la API directamente sin hacer una llamada HTTP
        data = {
            'nombre': nombre,
            'descripcion': descripcion
        }

        # Aquí se está asegurando de que el parámetro `modulo` se pase correctamente a la URL
        api_url = "http://localhost:5000/api/catalogo/agregar/?modulo=Materias"  # URL de la API
        
        # Realizar la petición a la API pasando los datos del formulario
        response = requests.post(api_url, json=data, cookies=request.cookies)
        
        # Verificamos la respuesta de la API
        if response.status_code == 201:
            flash("Materia agregada correctamente.", "success")
            return redirect(url_for('catalo.mostrar_materias'))  # Redirige a la lista de materias
        else:
            response_json = response.json()  # Accedemos a la respuesta JSON de la API
            error_message = response_json.get('error', 'Error desconocido')  # Obtenemos el mensaje de error
            flash(f"Error al agregar la materia: {error_message}", "danger")
            return redirect(url_for('catalo.agregar_materia'))  # Redirige al formulario en caso de error

    # Si el método es GET, mostramos el formulario
    context = {
        'form_title': 'Agregar Nueva Materia',
        'action_url': url_for('catalo.agregar_materia'),  # Ruta de acción del formulario
        'input_title': 'Nombre de la Materia',
        'desc_title': 'Descripción de la Materia',
        'button_text': 'Agregar Materia',
        'item_name': '',  # El valor inicial puede estar vacío
        'item_description': ''  # Lo mismo para la descripción
    }

    return render_template("materias/add_materia.jinja", **context)


@catalo_bp.route('/materias/editar/<int:materia_id>/', methods=['GET', 'POST'])
def editar_materia(materia_id):
    token = request.cookies.get("token")

    # Verificar si el token está presente
    if not token or token not in active_tokens:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('auth.login'))  # Redirige al login si no tiene sesión activa

    # Obtener el usuario desde el token
    user = get_user_from_token(token)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))  # Redirige al login si el usuario no existe

    # Verificamos el acceso al módulo de 'Materias'
    modulo = 'Materias'
    user_privilege, error = has_access_to_module(user, modulo)
    if error:  # Si no tiene acceso
        flash(error, "warning")
        return redirect(url_for('auth.index'))  # Redirige al index si no tiene acceso

    # Si el método es POST, procesamos el formulario
    if request.method == 'POST':
        can_edit = user_privilege.can_edit  # Verificamos si el usuario tiene permiso para editar
        if not can_edit:
            flash("No tienes permiso para editar una materia.", "warning")
            return redirect(url_for('auth.index'))  # Redirige al index si no tiene permiso de edición

        # Procesamos los datos del formulario
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']

        if not nombre or not descripcion:
            flash("Debe proporcionar nombre y descripción para la materia.", "warning")
            return redirect(url_for('catalo.editar_materia', materia_id=materia_id))  # Redirige si falta algún dato

        # Llamamos a la API para editar la materia
        data = {
            'id': materia_id,
            'nombre': nombre,
            'descripcion': descripcion
        }

        # Aquí se está asegurando de que el parámetro `modulo` se pase correctamente a la URL
        api_url = f"http://localhost:5000/api/catalogo/editar/?modulo=Materias"  # URL de la API

        # Realizar la petición a la API pasando los datos del formulario
        response = requests.put(api_url, json=data, cookies=request.cookies)

        # Verificamos la respuesta de la API
        if response.status_code == 200:
            flash("Materia editada correctamente.", "success")
            return redirect(url_for('catalo.mostrar_materias'))  # Redirige a la lista de materias
        else:
            response_json = response.json()  # Accedemos a la respuesta JSON de la API
            error_message = response_json.get('error', 'Error desconocido')  # Obtenemos el mensaje de error
            flash(f"Error al editar la materia: {error_message}", "danger")
            return redirect(url_for('catalo.editar_materia', materia_id=materia_id))  # Redirige al formulario en caso de error

    # Si el método es GET, obtenemos la materia a editar y mostramos el formulario
    materia = Materia.query.filter_by(id=materia_id, id_usuario=user.id).first()
    if not materia:
        flash("Materia no encontrada o no tienes acceso.", "danger")
        return redirect(url_for('catalo.mostrar_materias'))  # Redirige a la lista de materias si no existe

    context = {
        'form_title': 'Editar Materia',
        'action_url': url_for('catalo.editar_materia', materia_id=materia_id),  # Ruta de acción del formulario
        'input_title': 'Nombre de la Materia',
        'desc_title': 'Descripción de la Materia',
        'button_text': 'Editar Materia',
        'item_name': materia.nombre,  # Cargar el valor actual de la materia
        'item_description': materia.descripcion  # Lo mismo para la descripción
    }

    return render_template("materias/edit_materia.jinja", **context)


@catalo_bp.route('/materias/eliminar/<int:materia_id>/', methods=['POST'])
def eliminar_materia(materia_id):
    token = request.cookies.get("token")

    # Verificar si el token está presente
    if not token or token not in active_tokens:
        flash("Debes iniciar sesión para acceder a esta página.", "danger")
        return redirect(url_for('auth.login'))  # Redirige al login si no tiene sesión activa

    # Obtener el usuario desde el token
    user = get_user_from_token(token)
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('auth.login'))  # Redirige al login si el usuario no existe

    # Verificamos el acceso al módulo de 'Materias'
    modulo = 'Materias'
    user_privilege, error = has_access_to_module(user, modulo)
    if error:  # Si no tiene acceso
        flash(error, "warning")
        return redirect(url_for('auth.index'))  # Redirige al index si no tiene acceso

    # Verificar si tiene permiso para eliminar
    can_delete = user_privilege.can_delete
    if not can_delete:
        flash("No tienes permiso para eliminar una materia.", "warning")
        return redirect(url_for('auth.index'))  # Redirige al index si no tiene permiso de eliminación

    # Hacemos la solicitud DELETE a la API
    api_url = f"http://localhost:5000/api/catalogo/delete/?modulo=Materias"  # URL de la API
    data = {
        'id': materia_id
    }

    response = requests.delete(api_url, json=data, cookies=request.cookies)

    # Verificamos la respuesta de la API
    if response.status_code == 200:
        flash("Materia eliminada correctamente.", "success")
    else:
        response_json = response.json()  # Accedemos a la respuesta JSON de la API
        error_message = response_json.get('error', 'Error desconocido')  # Obtenemos el mensaje de error
        flash(f"Error al eliminar la materia: {error_message}", "danger")

    return redirect(url_for('catalo.mostrar_materias')) 