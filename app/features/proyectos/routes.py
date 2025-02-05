from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from app.middleware.auth_middleware import auth_required
from app.db.db import db
from app.db.proyectos_model import Proyectos

proyectos_bp = Blueprint('proyectos', __name__)

# Ruta para mostrar el formulario de agregar un nuevo proyecto
@proyectos_bp.route('/proyectos/agregar/', methods=['GET'])
@auth_required
def agregar_proyecto_form():
    return render_template("proyectos/add_proyecto.jinja")

# Ruta para mostrar los detalles de un proyecto específico
@proyectos_bp.route('/proyectos/detalle/<int:id>/', methods=['GET'])
@auth_required
def detalle_proyecto(id):
    proyecto = Proyectos.query.get_or_404(id)  # Obtener el proyecto por ID o devolver 404 si no existe
    return render_template("proyectos/detail_proyecto.jinja", proyecto=proyecto)

# Ruta para mostrar el formulario de editar un proyecto
@proyectos_bp.route('/proyectos/editar/<int:id>/', methods=['GET'])
@auth_required
def editar_proyecto_form(id):
    proyecto = Proyectos.query.get_or_404(id)  # Obtener el proyecto por ID o devolver 404 si no existe 