from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from app.middleware.auth_middleware import auth_required
from app.db.db import db
from app.db.Materias_model import Materia  # Asegúrate de importar el modelo Materia

materia_bp = Blueprint('materia', __name__)

# Ruta para mostrar el formulario de agregar una nueva materia
@materia_bp.route('/materia/agregar/', methods=['GET'])
@auth_required
def agregar_materia_form():
    return render_template("materia/add_materia.jinja")

# Ruta para mostrar los detalles de una materia específica
@materia_bp.route('/materia/detalle/<int:id>/', methods=['GET'])
@auth_required
def detalle_materia(id):
    materia = Materia.query.get_or_404(id)  # Obtener la materia por ID o devolver 404 si no existe
    return render_template("materia/detail_materia.jinja", materia=materia)

# Ruta para mostrar el formulario de editar una materia
@materia_bp.route('/materia/editar/<int:id>/', methods=['GET'])
@auth_required
def editar_materia_form(id):
    materia = Materia.query.get_or_404(id)  # Obtener la materia por ID o devolver 404 si no existe
    return render_template("materia/edit_materia.jinja", materia=materia)