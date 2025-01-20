from flask import Blueprint, render_template, url_for

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('index.jinja')

@auth.route('/tavo')  # Asegúrate de incluir la barra inicial '/'
def tavo():
    return render_template('temporary/tavo/index.jinja')

@auth.route('/tavo/juegos')  # Asegúrate de incluir la barra inicial '/'
def juegos():
    return render_template('temporary/tavo/juegos/index.jinja')


@auth.route('/tavo/materias')  # Asegúrate de incluir la barra inicial '/'
def materias():
    return render_template('temporary/tavo/materias/index.jinja')


@auth.route('/tavo/proyectos')  # Asegúrate de incluir la barra inicial '/'
def proyectos():
    return render_template('temporary/tavo/proyectos/index.jinja')


@auth.route('/jesus')  # Asegúrate de incluir la barra inicial '/'
def jesus():
    return render_template('temporary/jesus/index.jinja')

@auth.route('/jesus/juegos')  # Asegúrate de incluir la barra inicial '/'
def juegos_jesus():
    return render_template('temporary/jesus/juegos/index.jinja')

@auth.route('/jesus/materias')  # Asegúrate de incluir la barra inicial '/'
def materias_jesus():
    return render_template('temporary/jesus/materias/index.jinja')

@auth.route('/jesus/proyectos')  # Asegúrate de incluir la barra inicial '/'
def proyectos_jesus(): 
    return render_template('temporary/jesus/proyectos/index.jinja')

@auth.route('/jesus/error') 
def error_jesus():
    return render_template('errors/504.jinja')

