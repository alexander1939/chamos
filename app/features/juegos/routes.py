from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.features.juegos.model import Juegos
from app.db import db

juegos = Blueprint('juegos', __name__)


@juegos.get('/juegos')
@login_required
def listar_juegos():
    juegos = Juegos.query.filter_by(id_usuario=current_user.id).all()
    return render_template('juegos/index.jinja', user=current_user, juegos=juegos)



@juegos.get('/juegos/detalles/<int:juego_id>')
@login_required
def juego_detail(juego_id):
    juego = Juegos.query.get_or_404(juego_id)

    if juego.id_usuario != current_user.id:
        flash("No tienes permiso para ver esta materia.", "danger")
        return redirect(url_for('juegos.listar_juegos'))

    return render_template(
        'juegos/detail_juego.jinja',
        user=current_user,
        name=juego.nombre,
        description=juego.descripcion,
    )



@juegos.get('/juegos/agregar')
@login_required
def form_add_juego():
    return render_template(
        'juegos/add_juego.jinja',
        page_title="Agregar Juego",
        form_title="Formulario para agregar un nuevo Juego",
        input_title="Nombre del Juego",
        desc_title="Descripción del Juego",
        action_url=url_for('juegos.save_juego'),
        button_text="Agregar Juego",
        item_name="",
        item_description="",
        user=current_user
    )


@juegos.post('/juegos/agregar')
@login_required
def save_juego():
    nombre = request.form['item_name']
    descripcion = request.form.get('item_description', '')  
    
    nuevo_juego = Juegos(
        nombre=nombre,
        descripcion=descripcion,
        id_usuario=current_user.id  
    )

    try:
        db.session.add(nuevo_juego)
        db.session.commit()
        flash("Juego agregado exitosamente.", "success")
        return redirect(url_for('juegos.listar_juegos'))
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al agregar el juego. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
        return redirect(url_for('juegos.form_add_juego'))


@juegos.get('/juegos/editar/<int:juego_id>')
@login_required
def form_edit_juego(juego_id):
    juego = Juegos.query.get_or_404(juego_id)
    
    if juego.id_usuario != current_user.id:
        flash("No tienes permiso para editar este juego.", "danger")
        return redirect(url_for('juegos.listar_juegos'))
    
    return render_template(
        'juegos/edit_juego.jinja',
        page_title="Editar Juego",
        form_title="Formulario para editar el Juego",
        input_title="Nombre del Juego",
        desc_title="Descripción del Juego",
        action_url=url_for('juegos.save_edited_juego', juego_id=juego.id),
        button_text="Actualizar Juego",
        item_name=juego.nombre,
        item_description=juego.descripcion,
        user=current_user
    )
@juegos.post('/juegos/editar/<int:juego_id>')
@login_required
def save_edited_juego(juego_id):
    juego = Juegos.query.get_or_404(juego_id)

    if juego.id_usuario != current_user.id:
        flash("No tienes permiso para editar este juego.", "danger")
        return redirect(url_for('juegos.listar_juegos'))
    
    juego.nombre = request.form['item_name']
    juego.descripcion = request.form.get('item_description', '')  

    try:
        db.session.commit()
        flash("Juego actualizado exitosamente.", "success")
        return redirect(url_for('juegos.listar_juegos'))
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al actualizar el juego. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
        return redirect(url_for('juegos.form_edit_juego', juego_id=juego_id))


@juegos.post('/juegos/eliminar/<int:juego_id>')
@login_required
def delete_juego(juego_id):
    juego = Juegos.query.get_or_404(juego_id)
    
    if juego.id_usuario != current_user.id:
        flash("No tienes permiso para eliminar este juego.", "danger")
        return redirect(url_for('juegos.listar_juegos'))
    
    try:
        db.session.delete(juego)
        db.session.commit()
        flash("Juego eliminado exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Ocurrió un error al eliminar el juego. Inténtalo de nuevo.", "danger")
        print(f"Error: {e}")
    
    return redirect(url_for('juegos.listar_juegos'))                    