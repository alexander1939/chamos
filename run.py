from flask import Flask, render_template


from app import create_app

app = create_app()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.jinja'), 404

if __name__ == '__main__':
    app.run(debug=True)
