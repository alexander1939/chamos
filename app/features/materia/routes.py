from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.features.materia.model import Materia
from app.db import db
from app.features.auth.model import User
from app.features.juegos.model import Juegos
from app.features.proyectos.model import Proyectos
from sqlalchemy import or_




materia = Blueprint('materia', __name__)




@materia.route('/materias')
@login_required
def listar_materias():  
    if current_user.role == 'Mini':
        flash("No puedes agregar materias.", "warning")
        return redirect(url_for('auth.index'))
    user_materias = {}
    user_proyectos = {}
    user_juegos = {}
    users = []
    
    if current_user.role == 'Admin':    
        materias = Materia.query.all()
        proyectos = Proyectos.query.all()
        juegos = Juegos.query.all()

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
        materias = Materia.query.filter_by(id_usuario=current_user.id).all()
        proyectos = Proyectos.query.filter_by(id_usuario=current_user.id).all()
        juegos = Juegos.query.filter_by(id_usuario=current_user.id).all()

        user_materias[current_user.id] = materias
        user_proyectos[current_user.id] = proyectos
        user_juegos[current_user.id] = juegos
    
    return render_template(
        'materias/index.jinja', 
        user=current_user, 
        materias=materias, 
        proyectos=proyectos, 
        juegos=juegos, 
        user_materias=user_materias, 
        user_proyectos=user_proyectos, 
        user_juegos=user_juegos, 
        users=users 
    )


@materia.get('/materias/detalles/<int:materia_id>')
@login_required
def materia_detail(materia_id):
    materia = Materia.query.get_or_404(materia_id)

    if current_user.role != 'Admin' and materia.id_usuario != current_user.id:
        flash("No tienes permiso para ver esta materia.", "danger")
        return redirect(url_for('materia.listar_materias'))

    proyectos = Proyectos.query.filter_by(id_usuario=current_user.id).all()
    juegos = Juegos.query.filter_by(id_usuario=current_user.id).all()
    
    if current_user.role == 'Admin':
        users = User.query.filter(User.role != 'Admin').all()
        user_materias = {user.id: Materia.query.filter_by(id_usuario=user.id).all() for user in users}
        user_proyectos = {user.id: Proyectos.query.filter_by(id_usuario=user.id).all() for user in users}
        user_juegos = {user.id: Juegos.query.filter_by(id_usuario=user.id).all() for user in users}
    else:
        users = [current_user]
        user_materias = {current_user.id: Materia.query.filter_by(id_usuario=current_user.id).all()}
        user_proyectos = {current_user.id: Proyectos.query.filter_by(id_usuario=current_user.id).all()}
        user_juegos = {current_user.id: Juegos.query.filter_by(id_usuario=current_user.id).all()}

    return render_template(
        'materias/detail_materia.jinja',
        user=current_user,
        name=materia.nombre,
        description=materia.descripcion,
        users=users, 
        user_materias=user_materias,
        user_proyectos=user_proyectos, 
        user_juegos=user_juegos,
        proyectos=proyectos,
        juegos=juegos,
    )


@materia.get('/materias/agregar')
@login_required
def form_add_materia():
    if current_user.role == 'Admin' or current_user.role == 'Mini':
        flash("Los administradores no pueden agregar materias.", "warning")
        return redirect(url_for('auth.index'))
    
    proyectos = Proyectos.query.filter_by(id_usuario=current_user.id).all()
    juegos = Juegos.query.filter_by(id_usuario=current_user.id).all()

    user_materias = {current_user.id: Materia.query.filter_by(id_usuario=current_user.id).all()}
    
    return render_template(
        'materias/add_materia.jinja',
        page_title="Agregar Materia",
        form_title="Formulario para agregar una nueva Materia",
        input_title="Nombre de la Materia",
        desc_title="Descripción de la Materia",
        action_url=url_for('materia.save_materia'),
        button_text="Agregar Materia",
        item_name="",
        item_description="",
        user=current_user,
        user_materias=user_materias,
        proyectos=proyectos,
        juegos=juegos,
        user_proyectos={current_user.id: proyectos},
        user_juegos={current_user.id: juegos}
    )


@materia.post('/materias/agregar')
@login_required
def save_materia():
    if current_user.role == 'Admin' or current_user.role == 'Mini':
        flash("Los administradores no pueden agregar materias.", "warning")
        return redirect(url_for('auth.index'))

    nombre = request.form['item_name']
    descripcion = request.form.get('item_description', '')  

    nueva_materia = Materia(
        nombre=nombre,
        descripcion=descripcion,
        id_usuario=current_user.id  
    )

    try:
        db.session.add(nueva_materia)
        db.session.commit()
        flash("Materia agregada exitosamente.", "success")
        return redirect(url_for('materia.listar_materias'))
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al agregar la materia. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
        return redirect(url_for('materia.form_add_materia'))


@materia.get('/materias/editar/<int:materia_id>')
@login_required
def form_edit_materia(materia_id):
    if current_user.role == 'Admin' or current_user.role == 'Mini': 
        flash("Los administradores no pueden editar materias.", "warning")
        return redirect(url_for('auth.index'))

    materia = Materia.query.get_or_404(materia_id)

    if materia.id_usuario != current_user.id:
        flash("No tienes permiso para editar esta materia.", "danger")
        return redirect(url_for('materia.listar_materias'))

    proyectos = Proyectos.query.filter_by(id_usuario=current_user.id).all()
    juegos = Juegos.query.filter_by(id_usuario=current_user.id).all()

    return render_template(
        'materias/edit_materia.jinja',
        page_title="Editar Materia",
        form_title="Formulario para editar la Materia",
        input_title="Nombre de la Materia",
        desc_title="Descripción de la Materia",
        action_url=url_for('materia.save_edited_materia', materia_id=materia.id),
        button_text="Actualizar Materia",
        item_name=materia.nombre,
        item_description=materia.descripcion,
        user=current_user,
        proyectos=proyectos,
        juegos=juegos,
        user_proyectos={current_user.id: proyectos},
        user_juegos={current_user.id: juegos}
    )


@materia.post('/materias/editar/<int:materia_id>')
@login_required
def save_edited_materia(materia_id):
    if current_user.role == 'Admin' or current_user.role == 'Mini':  
        flash("Los administradores no pueden editar materias.", "warning")
        return redirect(url_for('auth.index'))

    materia = Materia.query.get_or_404(materia_id)

    if materia.id_usuario != current_user.id:
        flash("No tienes permiso para editar esta materia.", "danger")
        return redirect(url_for('materia.listar_materias'))
    
    materia.nombre = request.form['item_name']
    materia.descripcion = request.form.get('item_description', '')  

    try:
        db.session.commit()
        flash("Materia actualizada exitosamente.", "success")
        return redirect(url_for('materia.listar_materias'))
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al actualizar la materia. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
        return redirect(url_for('materia.form_edit_materia', materia_id=materia_id))


@materia.post('/materias/eliminar/<int:materia_id>')
@login_required
def delete_materia(materia_id):
    if current_user.role == 'Admin' or current_user.role == 'Mini':  
        flash("Los administradores no pueden eliminar materias.", "warning")
        return redirect(url_for('auth.index'))

    materia = Materia.query.get_or_404(materia_id)

    if materia.id_usuario != current_user.id:
        flash("No tienes permiso para eliminar esta materia.", "danger")
        return redirect(url_for('materia.listar_materias'))
    
    try:
        db.session.delete(materia)
        db.session.commit()
        flash("Materia eliminada exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al eliminar la materia. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
    
    return redirect(url_for('materia.listar_materias'))
