"""
Registro central das rotas da API.
"""

from api.routes.auth_routes import auth_bp
from api.routes.health_routes import health_bp
from api.routes.report_routes import report_bp
from api.routes.reservation_routes import reservation_bp
from api.routes.room_routes import room_bp
from api.routes.user_routes import user_bp


def register_routes(app):
    """
    Registra todos os blueprints da aplicação.
    """

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(room_bp, url_prefix="/api/rooms")
    app.register_blueprint(reservation_bp, url_prefix="/api/reservations")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(report_bp, url_prefix="/api/reports")