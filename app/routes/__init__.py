# from app.routes.platos import platos_bp
# from app.routes.pedidos import pedidos_bp
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.admin import admin_bp
from app.routes.chef import chef_bp
from app.routes.mesero import mesero_bp

def register_routes(app):
#     app.register_blueprint(platos_bp, url_prefix="/platos")
#     app.register_blueprint(pedidos_bp, url_prefix="/pedidos")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(chef_bp, url_prefix="/chef")
    app.register_blueprint(mesero_bp, url_prefix="/mesero")

