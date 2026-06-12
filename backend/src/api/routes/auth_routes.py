"""
Rotas de autenticação.
"""

from flask import Blueprint, request

from api.dependencies import get_auth_service, get_current_user
from api.responses import success_response
from api.schemas.auth_schema import LoginSchema, RegisterSchema


auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    """
    Autentica o usuário.
    """

    payload = request.get_json(silent=True) or {}
    data = LoginSchema.validate(payload)

    auth_service = get_auth_service()
    result = auth_service.login(
        email=data["email"],
        password=data["password"],
    )

    return success_response(
        data=result,
        status_code=200,
    )


@auth_bp.get("/me")
def me():
    """
    Retorna o usuário autenticado.
    """

    current_user = get_current_user()

    return success_response(
        data=current_user,
        status_code=200,
    )


@auth_bp.post("/logout")
def logout():
    """
    Encerra a sessão do usuário.
    """

    auth_service = get_auth_service()
    result = auth_service.logout()

    return success_response(
        data=result or {"message": "Logout realizado com sucesso."},
        status_code=200,
    )


@auth_bp.post("/register")
def register():
    """
    Registra um novo usuário.

    Use esta rota apenas se o sistema permitir cadastro público.
    """

    payload = request.get_json(silent=True) or {}
    data = RegisterSchema.validate(payload)

    auth_service = get_auth_service()
    user = auth_service.register(data)

    return success_response(
        data=user,
        status_code=201,
    )