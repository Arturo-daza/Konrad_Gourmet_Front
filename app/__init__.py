from flask import Flask, redirect, render_template, request, url_for
from app.config import Config
from app.extensions import db, migrate, jwt
from app.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # # Registrar rutas
    register_routes(app)
    @app.errorhandler(404)
    def page_not_found(e):
        if request.endpoint == 'auth.login':  # Cambia 'auth.login' según tu ruta
            return render_template('404.html'), 404  # Renderiza una página 404 personalizada
        return redirect(url_for('auth.login'))


    return app
