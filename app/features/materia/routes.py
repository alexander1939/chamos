from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.features.materia.model import Materia
from app.db import db

materia = Blueprint('materia', __name__)

@materia.route('/crear-materia/')
def crear_materia():
    return render_template('materias/materia.jinja',user=current_user)

