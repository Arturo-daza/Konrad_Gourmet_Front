from flask import Flask
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

    return app
