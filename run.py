from flask import Flask, render_template
from app import create_app
from dotenv import load_dotenv

# Cargar variables del .env antes de crear la app
load_dotenv()

# Crear la aplicación Flask
app = create_app()

# Manejo de error 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.jinja'), 404

# Punto de entrada principal
if __name__ == '__main__':
    app.run(debug=True)
