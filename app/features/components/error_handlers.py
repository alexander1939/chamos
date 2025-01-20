from flask import app,render_template

# Manejador para error 404 (Página no encontrada)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Manejador para error 500 (Error interno del servidor)
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Manejador genérico para otros códigos de error
@app.errorhandler(Exception)
def handle_exception(e):
    # Si el error tiene un código HTTP, lo usamos; de lo contrario, asumimos 500
    code = getattr(e, 'code', 500)
    return render_template('generic_error.html', error=e, code=code), code

@app.route('/cause-error')
def cause_error():
    # Genera un error para probar
    raise ValueError("Error provocado para pruebas.")