"""
Rotas de saúde da API.
"""

from flask import Blueprint

from api.responses import success_response


health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    """
    Verifica se a API está ativa.
    """

    return success_response(
        data={"status": "ok"},
        status_code=200,
    )