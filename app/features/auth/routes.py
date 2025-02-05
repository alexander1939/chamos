from flask import Blueprint, request, render_template,redirect,url_for,make_response
from flask import jsonify, request, render_template

from app.api.auth_api import register_user, login_user, logout_user, protected_route
from app.middleware.auth_middleware import  auth_required
from app.api.menu_api import get_user_menu
from app.middleware.auth_middleware import auth_required, guest_only
from app.db.db import db
from app.db.users_model import User
from app.db.Privilege_model import Privilege
from app.db.UserPrivilege_model import UserPrivilege
from werkzeug.security import generate_password_hash
from app.db.Juegos_model import Juegos
from app.db.materias_model import Materia
from app.db.proyectos_model import Proyectos
from app.db.UserPrivilege_model import UserPrivilege
from app.api.menu_api import get_user_menu

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@auth_required
def index():
    return render_template("index.jinja")


@auth_bp.get('/register/') 
@guest_only 
def register():
    return render_template("auth/register.jinja")


@auth_bp.get('/login/')
@guest_only
def login():
    return render_template("auth/login.jinja")

@auth_bp.get('/priv')
@auth_required
def priv():
    return render_template("auth/manage_priv.jinja")

@auth_bp.get('/con_users')
@auth_required
def consulta_usuarios():
    usuarios = [
        {
            'id': 1,
            'name': 'José',
            'surnames': 'Pérez López',
            'email': 'jose@example.com',
            'phone': '555-1234',
            'privilegios': [
                {'name': 'Materias'},
                {'name': 'Juegos'}
            ]
        },
        {
            'id': 2,
            'name': 'María',
            'surnames': 'García Sánchez',
            'email': 'maria@example.com',
            'phone': '555-5678',
            'privilegios': [
                {'name': 'Proyectos'}
            ]
        },
        {
            'id': 3,
            'name': 'Carlos',
            'surnames': 'Martínez Ruiz',
            'email': 'carlos@example.com',
            'phone': '555-9876',
            'privilegios': []
        }
    ]
    return render_template('auth/consulta_users.jinja', usuarios=usuarios)