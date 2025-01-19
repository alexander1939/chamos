from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return render_template('index.jinja')

@auth.route('/tavo/') 
def tavo():
    return render_template('temporary/tavo/index.jinja')

@auth.route('/tavo/juegos/')  
def juegos_tavo():
    return render_template('temporary/tavo/juegos/index.jinja')

@auth.route('/tavo/juegos/call-of-duty/')  
def juegos_tavo_call():
    return render_template('temporary/tavo/juegos/call.jinja')  

@auth.route('/tavo/juegos/fornite/')  
def juegos_tavo_fornite():
    return render_template('temporary/tavo/juegos/fornite.jinja')  

@auth.route('/tavo/juegos/free-fire/')  
def juegos_tavo_free():
    return render_template('temporary/tavo/juegos/free.jinja')  




@auth.route('/tavo/materias/')  
def materias_tavo():
    return render_template('temporary/tavo/materias/index.jinja')

@auth.route('/tavo/materias/matematicas/') 
def materias_tavo_mate():
    return render_template('temporary/tavo/materias/matematicas.jinja')


@auth.route('/tavo/materias/desrrollo-web/') 
def materias_tavo_desa():
    return render_template('temporary/tavo/materias/desarrollo_web.jinja')


@auth.route('/tavo/materias/empredimiento/') 
def materias_tavo_empre():
    return render_template('temporary/tavo/materias/empredimiento.jinja')




@auth.route('/tavo/proyectos/') 
def proyectos_tavo():
    return render_template('temporary/tavo/proyectos/index.jinja')


@auth.route('/tavo/proyectos/cuestionario/') 
def proyectos_tavo_cues():
    return render_template('temporary/tavo/proyectos/cuestionario.jinja')

@auth.route('/tavo/proyectos/mensajes/') 
def proyectos_tavo_mensa():
    return render_template('temporary/tavo/proyectos/mensajes.jinja')

@auth.route('/tavo/proyectos/tareas/') 
def proyectos_tavo_tareas():
    return render_template('temporary/tavo/proyectos/tareas.jinja')


@auth.route('/error-404')
def error_404():
    return render_template('errors/404.jinja')





