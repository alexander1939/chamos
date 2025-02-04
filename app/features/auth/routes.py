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