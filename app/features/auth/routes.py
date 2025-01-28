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
from app.features.materia.model import Materia
from app.features.proyectos.model import Proyectos
from app.features.juegos.model import Juegos
from sqlalchemy import or_




auth = Blueprint('auth', __name__)

@auth.route('/')
@login_required
def index():
    users = []
    user_materias = {}
    user_proyectos = {}
    user_juegos = {}

    if current_user.role == 'Admin':
        users = User.query.filter(
            or_(
                User.role == 'Usuario',
                User.role == 'Mini',
                User.role == 'Small'
            )
        ).all()



        for user in users:
            user_materias[user.id] = Materia.query.filter_by(id_usuario=user.id).all()  
            user_proyectos[user.id] = Proyectos.query.filter_by(id_usuario=user.id).all()  
            user_juegos[user.id] = Juegos.query.filter_by(id_usuario=user.id).all()  
    
    else:
        user_materias[current_user.id] = Materia.query.filter_by(id_usuario=current_user.id).all()  
        user_proyectos[current_user.id] = Proyectos.query.filter_by(id_usuario=current_user.id).all() 
        user_juegos[current_user.id] = Juegos.query.filter_by(id_usuario=current_user.id).all()  
    
    return render_template('index.jinja', 
                           user=current_user, 
                           users=users, 
                           user_materias=user_materias, 
                           user_proyectos=user_proyectos, 
                           user_juegos=user_juegos)




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




@auth.route('/profile/')
@login_required
def profile():
    return render_template('auth/profile.jinja', user=current_user)




@auth.route('/old-page')
def old_page():
    abort(410)



# Ruta que requiere autenticación
@auth.route('/protected')
def protected():
    auth = request.authorization
    if not auth or auth.username != 'admin' or auth.password != 'password':
        abort(401) 
    return "Acceso permitido a la página protegida."



#error 400

@auth.route('/error400')
def error_400():
    abort(400)

@auth.route('/procesar', methods=['POST'])
def procesar():
    campo = request.form.get('campo')
    if not campo.isdigit():  # Verifica si el valor no es un número
        abort(400)  # Error 400 si el campo no es un entero
    return "Datos procesados correctamente"

@auth.app_errorhandler(400)
def handle_400_error(error):
    return render_template('/errors/400.jinja'), 400