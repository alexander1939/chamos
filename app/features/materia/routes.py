from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from app.middleware.auth_middleware import auth_required
from app.db.db import db
from app.db.Materias_model import Materia# Asegúrate de importar el modelo Materia

materia_bp = Blueprint('materia', __name__)

# Ruta para mostrar el formulario de agregar una nueva materia
@materia_bp.route('/materia/', methods=['GET'])
@auth_required
def index():
    return render_template("materias/index.jinja")

@materia_bp.route('/materia/agregar/', methods=['GET'])
@auth_required
def agregar_materia_form():
    return render_template("materia/add_materia.jinja")

# Ruta para mostrar los detalles de una materia específica
@materia_bp.route('/materia/detalle/<int:id>/', methods=['GET'])
@auth_required
def detalle_materia(id):
    return render_template("materia/detail_materia.jinja")

# Ruta para mostrar el formulario de editar una materia
@materia_bp.route('/materia/editar/<int:id>/', methods=['GET'])
@auth_required
def editar_materia_form(id):
    return render_template("materia/edit_materia.jinja")