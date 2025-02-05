from flask import Blueprint, request, render_template, jsonify, redirect, url_for
from app.middleware.auth_middleware import auth_required
from app.db.db import db
from app.db.Juegos_model import Juegos

juegos_bp = Blueprint('juegos', __name__)

# Ruta para mostrar el formulario de agregar un nuevo juego
@juegos_bp.route('/juegos/agregar/', methods=['GET'])
@auth_required
def agregar_juego_form():
    return render_template("juegos/add_juego.jinja")

# Ruta para mostrar los detalles de un juego específico
@juegos_bp.route('/juegos/detalle/<int:id>/', methods=['GET'])
@auth_required
def detalle_juego(id):
    juego = Juegos.query.get_or_404(id)  # Obtener el juego por ID o devolver 404 si no existe
    return render_template("juegos/detail_juego.jinja", juego=juego)

# Ruta para mostrar el formulario de editar un juego
@juegos_bp.route('/juegos/editar/<int:id>/', methods=['GET'])
@auth_required
def editar_juego_form(id):
    juego = Juegos.query.get_or_404(id)  # Obtener el juego por ID o devolver 404 si no existe
    return render_template("juegos/edit_juego.jinja", juego=juego)