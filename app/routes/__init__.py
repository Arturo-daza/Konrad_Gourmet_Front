# from app.routes.platos import platos_bp
# from app.routes.pedidos import pedidos_bp
from app.routes.auth import auth_bp

def register_routes(app):
#     app.register_blueprint(platos_bp, url_prefix="/platos")
#     app.register_blueprint(pedidos_bp, url_prefix="/pedidos")
    app.register_blueprint(auth_bp, url_prefix="/auth")
