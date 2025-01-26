from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.features.materia.model import Materia
from app.db import db

materia = Blueprint('materia', __name__)


@materia.get('/materias')
@login_required
def listar_materias():
    materias = Materia.query.filter_by(id_usuario=current_user.id).all()
    return render_template('materias/index.jinja', user=current_user, materias=materias)



@materia.get('/materias/detalles/<int:materia_id>')
@login_required
def materia_detail(materia_id):
    materia = Materia.query.get_or_404(materia_id)

    if materia.id_usuario != current_user.id:
        flash("No tienes permiso para ver esta materia.", "danger")
        return redirect(url_for('materia.listar_materias'))

    return render_template(
        'materias/detail_materia.jinja',
        user=current_user,
        name=materia.nombre,
        description=materia.descripcion,
    )



@materia.get('/materias/agregar')
@login_required
def form_add_materia():
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
        user=current_user
    )


@materia.post('/materias/agregar')
@login_required
def save_materia():
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
    materia = Materia.query.get_or_404(materia_id)
    
    if materia.id_usuario != current_user.id:
        flash("No tienes permiso para editar esta materia.", "danger")
        return redirect(url_for('materia.listar_materias'))
    
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
        user=current_user
    )


@materia.post('/materias/editar/<int:materia_id>')
@login_required
def save_edited_materia(materia_id):
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


