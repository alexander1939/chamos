from flask import Blueprint, abort, render_template, request, url_for

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

@auth.route('/error-500')
def error_500():
    return render_template('errors/500.jinja')







@auth.route('/jesus/')  # Asegúrate de incluir la barra inicial '/'
def jesus():
    return render_template('temporary/jesus/index.jinja')



@auth.route('/jesus/juegos/')  # Asegúrate de incluir la barra inicial '/'
def juegos_jesus():
    return render_template('temporary/jesus/juegos/index.jinja')

@auth.route('/jesus/juegos/fornite/')  
def juegos_jesus_fornite():
    return render_template('temporary/jesus/juegos/fornite.jinja')  

@auth.route('/jesus/juegos/apex/')  
def juegos_jesus_apex():
    return render_template('temporary/jesus/juegos/apex.jinja')  

@auth.route('/jesus/juegos/cod/')  
def juegos_jesus_cod():
    return render_template('temporary/jesus/juegos/cod.jinja')



@auth.route('/jesus/materias/')  # Asegúrate de incluir la barra inicial '/'
def materias_jesus():
    return render_template('temporary/jesus/materias/index.jinja')

@auth.route('/jesus/materias/base/')  
def materias_jesus_base():
    return render_template('temporary/jesus/materias/base.jinja')

@auth.route('/jesus/materias/ingles/')  
def materias_jesus_ingles():
    return render_template('temporary/jesus/materias/ingles.jinja')

@auth.route('/jesus/materias/programacion/')  
def materias_jesus_programacion():
    return render_template('temporary/jesus/materias/programacion.jinja')



@auth.route('/jesus/proyectos/')  # Asegúrate de incluir la barra inicial '/'
def proyectos_jesus(): 
    return render_template('temporary/jesus/proyectos/index.jinja')

@auth.route('/jesus/proyectos/mg/')  # Asegúrate de incluir la barra inicial '/'
def proyectos_jesus_mg(): 
    return render_template('temporary/jesus/proyectos/mg.jinja')

@auth.route('/jesus/proyectos/biblioteca/')  # Asegúrate de incluir la barra inicial '/'
def proyectos_jesus_biblioteca(): 
    return render_template('temporary/jesus/proyectos/biblioteca.jinja')

@auth.route('/jesus/proyectos/butique/')  # Asegúrate de incluir la barra inicial '/'
def proyectos_jesus_butique(): 
    return render_template('temporary/jesus/proyectos/butique.jinja')



@auth.route('/gael/')  # Asegúrate de incluir la barra inicial '/'
def gael():
    return render_template('temporary/gael/index.jinja')



@auth.route('/gael/juegos/')  # Asegúrate de incluir la barra inicial '/'
def juegos_gael():
    return render_template('temporary/gael/juegos/index.jinja')

@auth.route('/gael/juegos/fornite/')  
def juegos_gael_fornite():
    return render_template('temporary/gael/juegos/fornite.jinja')  

@auth.route('/gael/juegos/metro/')  
def juegos_gael_metro():
    return render_template('temporary/gael/juegos/metro.jinja')  

@auth.route('/gael/juegos/cod/')  
def juegos_gael_cod():
    return render_template('temporary/gael/juegos/cod.jinja')



@auth.route('/gael/materias/')  # Asegúrate de incluir la barra inicial '/'
def materias_gael():
    return render_template('temporary/gael/materias/index.jinja')

@auth.route('/gael/materias/base/')  
def materias_gael_base():
    return render_template('temporary/gael/materias/base.jinja')

@auth.route('/gael/materias/ingles/')  
def materias_gael_ingles():
    return render_template('temporary/gael/materias/ingles.jinja')

@auth.route('/gael/materias/programacion/')  
def materias_gael_programacion():
    return render_template('temporary/gael/materias/programacion.jinja')



@auth.route('/gael/proyectos/')  # Asegúrate de incluir la barra inicial '/'
def proyectos_gael(): 
    return render_template('temporary/gael/proyectos/index.jinja')

@auth.route('/gael/proyectos/connectricity/')  # Asegúrate de incluir la barra inicial '/'
def proyectos_gael_connect(): 
    return render_template('temporary/gael/proyectos/connectricity.jinja')

@auth.route('/gael/proyectos/biblioteca/')  # Asegúrate de incluir la barra inicial '/'
def proyectos_gael_biblioteca(): 
    return render_template('temporary/gael/proyectos/biblioteca.jinja')

@auth.route('/gael/proyectos/butique/')  # Asegúrate de incluir la barra inicial '/'
def proyectos_gael_butique(): 
    return render_template('temporary/gael/proyectos/butique.jinja')

@auth.route('/error-504') 
def error_jesus():
    return render_template('errors/504.jinja')

@auth.route('/error-500') 
def error_gael():
    return render_template('errors/500.jinja')

