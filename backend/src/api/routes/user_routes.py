"""
Rotas de usuários.
"""

from flask import Blueprint, request

from api.dependencies import get_user_service
from api.guards.admin_guard import require_admin
from api.guards.auth_guard import require_auth
from api.responses import success_response
from api.schemas.user_schema import (
    CreateUserSchema,
    UpdateUserSchema,
    UserFilterSchema,
)


user_bp = Blueprint("users", __name__)


@user_bp.get("")
def list_users():
    """
    Lista usuários.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    filters = UserFilterSchema.validate(request.args.to_dict())

    user_service = get_user_service(current_user=current_user)
    users = user_service.list_users(filters=filters)

    return success_response(
        data=users,
        status_code=200,
    )


@user_bp.get("/<int:user_id>")
def get_user(user_id):
    """
    Busca um usuário por ID.
    """

    current_user = require_auth()

    user_service = get_user_service(current_user=current_user)
    user = user_service.get_user_by_id(user_id)

    return success_response(
        data=user,
        status_code=200,
    )


@user_bp.post("")
def create_user():
    """
    Cria um usuário.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    payload = request.get_json(silent=True) or {}
    data = CreateUserSchema.validate(payload)

    user_service = get_user_service(current_user=current_user)
    user = user_service.create_user(data)

    return success_response(
        data=user,
        status_code=201,
    )


@user_bp.put("/<int:user_id>")
def update_user(user_id):
    """
    Atualiza um usuário.
    """

    current_user = require_auth()

    payload = request.get_json(silent=True) or {}
    data = UpdateUserSchema.validate(payload)

    user_service = get_user_service(current_user=current_user)
    user = user_service.update_user(
        user_id=user_id,
        data=data,
    )

    return success_response(
        data=user,
        status_code=200,
    )


@user_bp.patch("/<int:user_id>/deactivate")
def deactivate_user(user_id):
    """
    Desativa um usuário.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    user_service = get_user_service(current_user=current_user)
    user = user_service.deactivate_user(user_id)

    return success_response(
        data=user,
        status_code=200,
    )


@user_bp.patch("/<int:user_id>/activate")
def activate_user(user_id):
    """
    Ativa um usuário.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    user_service = get_user_service(current_user=current_user)
    user = user_service.activate_user(user_id)

    return success_response(
        data=user,
        status_code=200,
    )