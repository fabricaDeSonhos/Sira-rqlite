"""
Rotas de salas.
"""

from flask import Blueprint, request

from api.dependencies import get_room_service
from api.guards.admin_guard import require_admin
from api.guards.auth_guard import require_auth
from api.responses import success_response
from api.schemas.room_schema import (
    CreateRoomSchema,
    RoomFilterSchema,
    UpdateRoomSchema,
)


room_bp = Blueprint("rooms", __name__)


@room_bp.get("")
def list_rooms():
    """
    Lista salas com filtros opcionais.
    """

    filters = RoomFilterSchema.validate(request.args.to_dict())

    room_service = get_room_service()
    rooms = room_service.list_rooms(filters=filters)

    return success_response(
        data=rooms,
        status_code=200,
    )


@room_bp.get("/<int:room_id>")
def get_room(room_id):
    """
    Busca uma sala por ID.
    """

    room_service = get_room_service()
    room = room_service.get_room_by_id(room_id)

    return success_response(
        data=room,
        status_code=200,
    )


@room_bp.post("")
def create_room():
    """
    Cria uma nova sala.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    payload = request.get_json(silent=True) or {}
    data = CreateRoomSchema.validate(payload)

    room_service = get_room_service(current_user=current_user)
    room = room_service.create_room(data)

    return success_response(
        data=room,
        status_code=201,
    )


@room_bp.put("/<int:room_id>")
def update_room(room_id):
    """
    Atualiza uma sala existente.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    payload = request.get_json(silent=True) or {}
    data = UpdateRoomSchema.validate(payload)

    room_service = get_room_service(current_user=current_user)
    room = room_service.update_room(
        room_id=room_id,
        data=data,
    )

    return success_response(
        data=room,
        status_code=200,
    )


@room_bp.patch("/<int:room_id>/deactivate")
def deactivate_room(room_id):
    """
    Desativa uma sala.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    room_service = get_room_service(current_user=current_user)
    room = room_service.deactivate_room(room_id)

    return success_response(
        data=room,
        status_code=200,
    )


@room_bp.patch("/<int:room_id>/activate")
def activate_room(room_id):
    """
    Ativa uma sala.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    room_service = get_room_service(current_user=current_user)
    room = room_service.activate_room(room_id)

    return success_response(
        data=room,
        status_code=200,
    )