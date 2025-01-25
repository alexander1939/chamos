from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from flask_login import login_user
from flask_login import login_required, logout_user,  current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.features.auth.model import User
from app.features.auth.form import RegisterForm, LoginForm
from app.db import db
from flask_login import login_user
from werkzeug.security import check_password_hash
from flask_login import login_required, logout_user,  current_user

auth = Blueprint('auth', __name__)

@auth.get('/register/')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    context = {
        "register_form": RegisterForm()
    }
    return render_template('auth/register.jinja', **context)


@auth.post('/register/')
def register_post():
    form = RegisterForm()
    if not form.validate_on_submit():
        flash("Por favor, completa todos los campos requeridos.", "danger")
        return render_template('auth/register.jinja', register_form=form)

    existing_user = User.query.filter_by(email=form.email.data).first()
    if existing_user:
        flash("El correo ya está en uso. Por favor, utiliza otro.", "danger")
        return render_template('auth/register.jinja', register_form=form)
    
    try:
        user = User(
            name=form.name.data,
            surnames=form.surnames.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            role='Usuario',
            phone=form.phone.data
        )
        db.session.add(user)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('auth.login'))
    except Exception as e:
        db.session.rollback()
        flash(f"Error al registrar el usuario: {str(e)}", "danger")
        return render_template('auth/register.jinja', register_form=form)

@auth.get('/login/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    context = {
        "login_form": LoginForm()
    }
    return render_template('auth/login.jinja', **context)

@auth.post('/login/')
def login_post():
    form = LoginForm()
    if not form.validate_on_submit():
        flash("Por favor, completa todos los campos requeridos.", "danger")
        return render_template('auth/login.jinja', login_form=form)

    # Corregir la asignación del usuario
    user = User.query.filter_by(email=form.email.data).first()
    if user and check_password_hash(user.password, form.password.data):
        login_user(user)
        flash("Inicio de sesión exitoso.", "success")
        return redirect(url_for('auth.index'))

    flash("Correo o contraseña incorrectos.", "danger")
    return render_template('auth/login.jinja', login_form=form)




@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('auth.login'))



@auth.route('/')
@login_required
def index():
    return render_template('index.jinja', user=current_user)



@auth.route('/profile/')
@login_required
def profile():
    return render_template('auth/profile.jinja', user=current_user)




@auth.route('/tavo/')
@login_required
def tavo():
    return render_template('temporary/tavo/index.jinja', user=current_user)

@auth.route('/tavo/juegos/')
@login_required
def juegos_tavo():
    return render_template('temporary/tavo/juegos/index.jinja', user=current_user)

@auth.route('/tavo/juegos/call-of-duty/')
@login_required
def juegos_tavo_call():
    return render_template('temporary/tavo/juegos/call.jinja', user=current_user)

@auth.route('/tavo/juegos/fornite/')
@login_required
def juegos_tavo_fornite():
    return render_template('temporary/tavo/juegos/fornite.jinja', user=current_user)

@auth.route('/tavo/juegos/free-fire/')
@login_required
def juegos_tavo_free():
    return render_template('temporary/tavo/juegos/free.jinja', user=current_user)

@auth.route('/tavo/materias/')
@login_required
def materias_tavo():
    return render_template('temporary/tavo/materias/index.jinja', user=current_user)

@auth.route('/tavo/materias/matematicas/')
@login_required
def materias_tavo_mate():
    return render_template('temporary/tavo/materias/matematicas.jinja', user=current_user)

@auth.route('/tavo/materias/desrrollo-web/')
@login_required
def materias_tavo_desa():
    return render_template('temporary/tavo/materias/desarrollo_web.jinja', user=current_user)

@auth.route('/tavo/materias/empredimiento/')
@login_required
def materias_tavo_empre():
    return render_template('temporary/tavo/materias/empredimiento.jinja', user=current_user)

@auth.route('/tavo/proyectos/')
@login_required
def proyectos_tavo():
    return render_template('temporary/tavo/proyectos/index.jinja', user=current_user)

@auth.route('/tavo/proyectos/cuestionario/')
@login_required
def proyectos_tavo_cues():
    return render_template('temporary/tavo/proyectos/cuestionario.jinja', user=current_user)

@auth.route('/tavo/proyectos/mensajes/')
@login_required
def proyectos_tavo_mensa():
    return render_template('temporary/tavo/proyectos/mensajes.jinja', user=current_user)

@auth.route('/tavo/proyectos/tareas/')
@login_required
def proyectos_tavo_tareas():
    return render_template('temporary/tavo/proyectos/tareas.jinja', user=current_user)









@auth.route('/jesus/')
@login_required
def jesus():
    return render_template('temporary/jesus/index.jinja', user=current_user)

@auth.route('/jesus/juegos/')
@login_required
def juegos_jesus():
    return render_template('temporary/jesus/juegos/index.jinja', user=current_user)

@auth.route('/jesus/juegos/fornite/')
@login_required
def juegos_jesus_fornite():
    return render_template('temporary/jesus/juegos/fornite.jinja', user=current_user)

@auth.route('/jesus/juegos/apex/')
@login_required
def juegos_jesus_apex():
    return render_template('temporary/jesus/juegos/apex.jinja', user=current_user)

@auth.route('/jesus/juegos/cod/')
@login_required
def juegos_jesus_cod():
    return render_template('temporary/jesus/juegos/cod.jinja', user=current_user)

@auth.route('/jesus/materias/')
@login_required
def materias_jesus():
    return render_template('temporary/jesus/materias/index.jinja', user=current_user)

@auth.route('/jesus/materias/base/')
@login_required
def materias_jesus_base():
    return render_template('temporary/jesus/materias/base.jinja', user=current_user)

@auth.route('/jesus/materias/ingles/')
@login_required
def materias_jesus_ingles():
    return render_template('temporary/jesus/materias/ingles.jinja', user=current_user)

@auth.route('/jesus/materias/programacion/')
@login_required
def materias_jesus_programacion():
    return render_template('temporary/jesus/materias/programacion.jinja', user=current_user)

@auth.route('/jesus/proyectos/')
@login_required
def proyectos_jesus():
    return render_template('temporary/jesus/proyectos/index.jinja', user=current_user)

@auth.route('/jesus/proyectos/mg/')
@login_required
def proyectos_jesus_mg():
    return render_template('temporary/jesus/proyectos/mg.jinja', user=current_user)

@auth.route('/jesus/proyectos/biblioteca/')
@login_required
def proyectos_jesus_biblioteca():
    return render_template('temporary/jesus/proyectos/biblioteca.jinja', user=current_user)

@auth.route('/jesus/proyectos/butique/')
@login_required
def proyectos_jesus_butique():
    return render_template('temporary/jesus/proyectos/butique.jinja', user=current_user)

@auth.route('/old-page')
def old_page():
    abort(410)

@auth.route('/gael/')  # Asegúrate de incluir la barra inicial '/'
def gael():
    return render_template('temporary/gael/index.jinja', user=current_user)

@auth.route('/gael/juegos/')
@login_required
def juegos_gael():
    return render_template('temporary/juegos/index.jinja', user=current_user)

@auth.route('/gael/juegos/fornite/')
@login_required
def juegos_gael_fornite():
    return render_template('temporary/gael/juegos/fornite.jinja', user=current_user)

@auth.route('/gael/juegos/metro/')
@login_required
def juegos_gael_metro():
    return render_template('temporary/gael/juegos/metro.jinja', user=current_user)

@auth.route('/gael/juegos/cod/')
@login_required
def juegos_gael_cod():
    return render_template('temporary/gael/juegos/cod.jinja', user=current_user)

@auth.route('/gael/materias/')
@login_required
def materias_gael():
    return render_template('temporary/gael/materias/index.jinja', user=current_user)

@auth.route('/gael/materias/base/')
@login_required
def materias_gael_base():
    return render_template('temporary/gael/materias/base.jinja', user=current_user)

@auth.route('/gael/materias/ingles/')
@login_required
def materias_gael_ingles():
    return render_template('temporary/gael/materias/ingles.jinja', user=current_user)

@auth.route('/gael/materias/programacion/')
@login_required
def materias_gael_programacion():
    return render_template('temporary/gael/materias/programacion.jinja', user=current_user)

@auth.route('/gael/proyectos/')
@login_required
def proyectos_gael():
    return render_template('temporary/gael/proyectos/index.jinja', user=current_user)


@auth.route('/gael/proyectos/connectricity/')
@login_required  # Asegúrate de incluir la barra inicial '/'
def proyectos_gael_connect(): 
    return render_template('temporary/gael/proyectos/connectricity.jinja', user=current_user)

@auth.route('/gael/proyectos/biblioteca/') 
@login_required # Asegúrate de incluir la barra inicial '/'
def proyectos_gael_biblioteca(): 
    return render_template('temporary/gael/proyectos/biblioteca.jinja',user=current_user)

@auth.route('/gael/proyectos/butique/')
@login_required  # Asegúrate de incluir la barra inicial '/'
def proyectos_gael_butique(): 
    return render_template('temporary/gael/proyectos/butique.jinja',user=current_user)

@auth.route('/error-504') 
def error_jesus():
    return render_template('errors/504.jinja')


# Ruta que requiere autenticación
@auth.route('/protected')
def protected():
    auth = request.authorization
    if not auth or auth.username != 'admin' or auth.password != 'password':
        abort(401)  # Genera el error 401 si no se proporciona autenticación válida
    return "Acceso permitido a la página protegida."




@auth.route('/roberto/')
@login_required
def roberto():
    return render_template('temporary/roberto/index.jinja', user=current_user)

@auth.route('/roberto/juegos/')
@login_required
def juegos_roberto():
    return render_template('temporary/roberto/juegos/index.jinja', user=current_user)

@auth.route('/roberto/juegos/fortnite/')
@login_required
def juegos_roberto_fortnite():
    return render_template('temporary/roberto/juegos/fortnite.jinja', user=current_user)

@auth.route('/roberto/juegos/frefire/')
@login_required
def juegos_roberto_free():
    return render_template('temporary/roberto/juegos/freefire.jinja', user=current_user)

@auth.route('/roberto/juegos/clash/')
@login_required
def juegos_roberto_clash():
    return render_template('temporary/roberto/juegos/clashroyale.jinja', user=current_user)

@auth.route('/roberto/materias/')
@login_required
def materias_roberto():
    return render_template('temporary/roberto/materias/index.jinja', user=current_user)

@auth.route('/roberto/materias/base/')
@login_required
def materias_roberto_base():
    return render_template('temporary/roberto/materias/basedatos.jinja', user=current_user)

@auth.route('/roberto/materias/ingles/')
@login_required
def materias_roberto_ingles():
    return render_template('temporary/roberto/materias/ingles.jinja', user=current_user)

@auth.route('/roberto/materias/desarrollo/')
@login_required
def materias_roberto_des():
    return render_template('temporary/roberto/materias/desarrolloweb.jinja', user=current_user)

@auth.route('/roberto/proyectos/')
@login_required
def proyectos_roberto():
    return render_template('temporary/roberto/proyectos/index.jinja', user=current_user)

@auth.route('/roberto/proyectos/agencia/')
@login_required
def proyectos_roberto_age():
    return render_template('temporary/roberto/proyectos/agenciamoto.jinja', user=current_user)

@auth.route('/roberto/proyectos/evaluacion/')
@login_required
def proyectos_roberto_eva():
    return render_template('temporary/roberto/proyectos/udm.jinja', user=current_user)

@auth.route('/roberto/proyectos/puntoventa/')
@login_required
def proyectos_roberto_punto():
    return render_template('temporary/roberto/proyectos/asscom.jinja', user=current_user)


# RUTA PARA FORMULARIOS DINAMICOS
# Variables globales para almacenar los datos temporalmente
user_games = {}
user_projects = {}
user_subjects = {}

@auth.route('/juegos/agregarJuego', methods=['GET', 'POST'])
@login_required
def add_game():
    if request.method == 'POST':
        name = request.form['item_name']
        description = request.form['item_description']
        # Asociar el juego con el usuario autenticado
        user_games.setdefault(current_user.id, []).append({
            'name': name,
            'description': description
        })
        flash("Juego agregado exitosamente.", "success")
        return redirect(url_for('auth.games'))  # Redirigir a la lista de juegos

    # Enviar datos al formulario
    return render_template(
        'temporary/juegos/add_game.jinja',
        page_title="Agregar Juego",  # Título de la página
        form_title="Formulario para agregar un nuevo juego",  # Título del formulario
        input_title="Nombre del juego", # Título del campo
        desc_title="Descripción del juego", # Título de la descripcion
        action_url=url_for('auth.add_game'),  # URL de acción
        button_text="Agregar Juego",  # Texto del botón
        user=current_user,  # Información del usuario autenticado
        item_name="",  # Inicializa los campos del formulario
        item_description=""  # Inicializa los campos del formulario
    )

@auth.route('/juegos/detalles/<int:game_id>')
@login_required
def game_detail(game_id):
    # Obtener el juego de la lista temporal usando el game_id
    games = user_games.get(current_user.id, [])
    
    # Verificar si el game_id es válido (es decir, si está dentro del rango de la lista)
    if game_id <= 0 or game_id > len(games):
        flash("Juego no encontrado.", "danger")
        return redirect(url_for('auth.games'))  # Redirigir a la lista de juegos si no se encuentra
    
    # Acceder al juego correcto (el índice es game_id - 1 porque la lista comienza en 0)
    game = games[game_id - 1]  # Restamos 1 para convertir el game_id (1-indexed) a un índice (0-indexed)
    
    if not game:
        flash("Juego no encontrado.", "danger")
        return redirect(url_for('auth.games'))  # Redirigir a la lista de juegos si no se encuentra
    
    return render_template(
        'temporary/juegos/game_detail.jinja', user=current_user, 
        name=game['name'], 
        description=game['description']
    )



@auth.route('/juegos', methods=['GET'])
@login_required
def games():
    games = user_games.get(current_user.id, [])  # Obtener los juegos del usuario
    return render_template('temporary/juegos/index.jinja', user=current_user, games=games)

#EDITAR JUEGO
@auth.route('/edit_game/<int:game_id>', methods=['GET', 'POST'])
@login_required
def edit_game(game_id):
    # Obtener el juego de la lista temporal
    games = user_games.get(current_user.id, [])
    
    if game_id <= 0 or game_id > len(games):
        flash("Juego no encontrado.", "danger")
        return redirect(url_for('auth.games'))  # Redirigir a la lista de juegos si no se encuentra
    
    # Acceder al juego que se desea editar
    game = games[game_id - 1]
    
    # Si el formulario es enviado
    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form['item_name']
        description = request.form['item_description']
        
        # Actualizar los datos del juego
        game['name'] = name
        game['description'] = description
        
        flash("Juego actualizado exitosamente.", "success")
        return redirect(url_for('auth.games', game_id=game_id))  # Redirigir a la página de detalles del juego
    
    return render_template(
        'temporary/juegos/edit_game.jinja', user=current_user, 
        game=game,  # Enviar el juego a la plantilla
        page_title="Editar Juego",  # Título de la página
        form_title="Formulario para editar el juego",  # Título del formulario
        input_title="Nombre del juego",  # Título del campo de nombre
        desc_title="Descripción del juego",  # Título del campo de descripción
        action_url=url_for('auth.edit_game', game_id=game_id),  # URL de acción para el formulario
        button_text="Actualizar Juego"  # Texto del botón
    )

#ELIMINAR JUEGO
@auth.route('/delete_game/<int:game_id>', methods=['POST'])
@login_required
def delete_game(game_id):
    # Obtener la lista de juegos del usuario
    games = user_games.get(current_user.id, [])
    
    if game_id <= 0 or game_id > len(games):
        flash("Juego no encontrado.", "danger")
        return redirect(url_for('auth.games'))  # Redirigir a la lista de juegos si no se encuentra
    
    # Eliminar el juego de la lista
    games.pop(game_id - 1)
    
    flash("Juego eliminado exitosamente.", "success")
    return redirect(url_for('auth.games'))  # Redirigir a la lista de juegos
