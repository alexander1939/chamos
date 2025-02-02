from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.features.proyectos.model import Proyectos
from app.db import db
from app.features.materia.model import Materia
from app.features.juegos.model import Juegos
from sqlalchemy import or_




proyectos = Blueprint('proyectos', __name__)


@proyectos.route('/proyectos')
@login_required
def listar_proyectos():
    if current_user.role == 'Small':
        flash("No puedes agregar materias.", "warning")
        return redirect(url_for('auth.index'))

    user_materias = {}
    user_proyectos = {}
    user_juegos = {}
    users = []
    
    if current_user.role == 'Admin':    
        proyectos = Proyectos.query.all()
        materias = Materia.query.all()
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
        proyectos = Proyectos.query.filter_by(id_usuario=current_user.id).all()
        materias = Materia.query.filter_by(id_usuario=current_user.id).all()
        juegos = Juegos.query.filter_by(id_usuario=current_user.id).all()

        user_materias[current_user.id] = materias
        user_proyectos[current_user.id] = proyectos
        user_juegos[current_user.id] = juegos
    
    return render_template(
        'proyectos/index.jinja', 
        user=current_user, 
        proyectos=proyectos,
        materias=materias,
        juegos=juegos,
        user_materias=user_materias, 
        user_proyectos=user_proyectos, 
        user_juegos=user_juegos, 
        users=users 
    )


@proyectos.get('/proyectos/detalles/<int:proyecto_id>')
@login_required
def proyecto_detail(proyecto_id):
    if current_user.role == 'Small':
        flash("No puedes agregar materias.", "warning")
        return redirect(url_for('auth.index'))

    proyecto = Proyectos.query.get_or_404(proyecto_id)

    if current_user.role != 'Admin' and proyecto.id_usuario != current_user.id:
        flash("No tienes permiso para ver este proyecto.", "danger")
        return redirect(url_for('proyectos.listar_proyectos'))

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
        'proyectos/detail_proyecto.jinja',
        user=current_user,
        name=proyecto.nombre,
        description=proyecto.descripcion,
        users=users,
        user_materias=user_materias,
        user_proyectos=user_proyectos,
        user_juegos=user_juegos,
        proyectos=proyectos,
        juegos=juegos
    )


@proyectos.get('/proyectos/agregar')
@login_required
def form_add_proyecto():
    if current_user.role == 'Small':
        flash("No puedes agregar materias.", "warning")
        return redirect(url_for('auth.index'))
    if current_user.role == 'Admin':
        flash("Los administradores no pueden agregar proyectos.", "warning")
        return redirect(url_for('proyectos.listar_proyectos'))

    return render_template(
        'proyectos/add_proyecto.jinja',
        page_title="Agregar Proyecto",
        form_title="Formulario para agregar un nuevo Proyecto",
        input_title="Nombre del Proyecto",
        desc_title="Descripción del Proyecto",
        action_url=url_for('proyectos.save_proyecto'),
        button_text="Agregar Proyecto",
        item_name="",
        item_description="",
        user=current_user
    )


@proyectos.post('/proyectos/agregar')
@login_required
def save_proyecto():
    if current_user.role == 'Small':
        flash("No puedes agregar materias.", "warning")
        return redirect(url_for('auth.index'))
    if current_user.role == 'Admin':
        flash("Los administradores no pueden agregar proyectos.", "warning")
        return redirect(url_for('auth.index'))

    nombre = request.form['item_name']
    descripcion = request.form.get('item_description', '')  
    
    nuevo_proyecto = Proyectos(
        nombre=nombre,
        descripcion=descripcion,
        id_usuario=current_user.id  
    )

    try:
        db.session.add(nuevo_proyecto)
        db.session.commit()
        flash("Proyecto agregado exitosamente.", "success")
        return redirect(url_for('proyectos.listar_proyectos'))
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al agregar el proyecto. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
        return redirect(url_for('proyectos.form_add_proyecto'))


@proyectos.get('/proyectos/editar/<int:proyecto_id>')
@login_required
def form_edit_proyecto(proyecto_id):
    if current_user.role == 'Admin' or current_user.role== 'Small':
        flash("Los administradores no pueden editar proyectos.", "warning")
        return redirect(url_for('auth.index'))

    proyecto = Proyectos.query.get_or_404(proyecto_id)

    if proyecto.id_usuario != current_user.id:
        flash("No tienes permiso para editar este proyecto.", "danger")
        return redirect(url_for('proyectos.listar_proyectos'))

    return render_template(
        'proyectos/edit_proyecto.jinja',
        page_title="Editar Proyecto",
        form_title="Formulario para editar el Proyecto",
        input_title="Nombre del Proyecto",
        desc_title="Descripción del Proyecto",
        action_url=url_for('proyectos.save_edited_proyecto', proyecto_id=proyecto.id),
        button_text="Actualizar Proyecto",
        item_name=proyecto.nombre,
        item_description=proyecto.descripcion,
        user=current_user
    )


@proyectos.post('/proyectos/editar/<int:proyecto_id>')
@login_required
def save_edited_proyecto(proyecto_id):
    if current_user.role == 'Admin' or current_user.role == 'Small':
        flash("Los administradores no pueden editar proyectos.", "warning")
        return redirect(url_for('auth.index'))

    proyecto = Proyectos.query.get_or_404(proyecto_id)

    if proyecto.id_usuario != current_user.id:
        flash("No tienes permiso para editar este proyecto.", "danger")
        return redirect(url_for('proyectos.listar_proyectos'))

    proyecto.nombre = request.form['item_name']
    proyecto.descripcion = request.form.get('item_description', '')  

    try:
        db.session.commit()
        flash("Proyecto actualizado exitosamente.", "success")
        return redirect(url_for('proyectos.listar_proyectos'))
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al actualizar el proyecto. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
        return redirect(url_for('proyectos.form_edit_proyecto', proyecto_id=proyecto_id))


@proyectos.post('/proyectos/eliminar/<int:proyecto_id>')
@login_required
def delete_proyecto(proyecto_id):
    if current_user.role == 'Admin' or current_user.role == 'Small':
        flash("Los administradores no pueden eliminar proyectos.", "warning")
        return redirect(url_for('auth.index'))

    proyecto = Proyectos.query.get_or_404(proyecto_id)

    if proyecto.id_usuario != current_user.id:
        flash("No tienes permiso para eliminar este proyecto.", "danger")
        return redirect(url_for('proyectos.listar_proyectos'))

    try:
        db.session.delete(proyecto)
        db.session.commit()
        flash("Proyecto eliminado exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al eliminar el proyecto. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
    
    return redirect(url_for('proyectos.listar_proyectos'))

