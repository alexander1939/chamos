from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.features.proyectos.model import Proyectos
from app.db import db

proyectos = Blueprint('proyectos', __name__)


@proyectos.get('/proyectos')
@login_required
def listar_proyectos():
    proyectos = Proyectos.query.filter_by(id_usuario=current_user.id).all()
    return render_template('proyectos/index.jinja', user=current_user, proyectos=proyectos)



@proyectos.get('/proyectos/detalles/<int:proyecto_id>')
@login_required
def proyecto_detail(proyecto_id):
    proyecto = Proyectos.query.get_or_404(proyecto_id)

    if proyecto.id_usuario != current_user.id:
        flash("No tienes permiso para ver esta materia.", "danger")
        return redirect(url_for('proyectos.listar_proyectos'))

    return render_template(
        'proyectos/detail_proyecto.jinja',
        user=current_user,
        name=proyecto.nombre,
        description=proyecto.descripcion,
    )



@proyectos.get('/proyectos/agregar')
@login_required
def form_add_proyecto():
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