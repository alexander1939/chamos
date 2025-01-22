from flask import render_template

def init_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.jinja'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.jinja'), 500

def init_error_handlers(app):
    @app.errorhandler(403)
    def forbidden_error(e):
        return render_template('403.jinja'), 403

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('errors/401.jinja'), 401
