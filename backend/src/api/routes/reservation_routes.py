"""
Rotas de reservas.
"""

from flask import Blueprint, request

from api.dependencies import get_reservation_service
from api.guards.auth_guard import require_auth
from api.responses import success_response
from api.schemas.reservation_schema import (
    CreateReservationSchema,
    ReservationFilterSchema,
    UpdateReservationSchema,
)


reservation_bp = Blueprint("reservations", __name__)


@reservation_bp.get("")
def list_reservations():
    """
    Lista reservas com filtros opcionais.
    """

    current_user = require_auth()
    filters = ReservationFilterSchema.validate(request.args.to_dict())

    reservation_service = get_reservation_service(current_user=current_user)
    reservations = reservation_service.list_reservations(filters=filters)

    return success_response(
        data=reservations,
        status_code=200,
    )


@reservation_bp.get("/me")
def list_my_reservations():
    """
    Lista reservas do usuário autenticado.
    """

    current_user = require_auth()

    reservation_service = get_reservation_service(current_user=current_user)
    reservations = reservation_service.list_my_reservations()

    return success_response(
        data=reservations,
        status_code=200,
    )


@reservation_bp.get("/<int:reservation_id>")
def get_reservation(reservation_id):
    """
    Busca uma reserva por ID.
    """

    current_user = require_auth()

    reservation_service = get_reservation_service(current_user=current_user)
    reservation = reservation_service.get_reservation_by_id(reservation_id)

    return success_response(
        data=reservation,
        status_code=200,
    )


@reservation_bp.post("")
def create_reservation():
    """
    Cria uma nova reserva.

    O usuário vem da autenticação, não do payload.
    """

    current_user = require_auth()

    payload = request.get_json(silent=True) or {}
    data = CreateReservationSchema.validate(payload)

    reservation_service = get_reservation_service(current_user=current_user)
    reservation = reservation_service.create_reservation(data=data)

    return success_response(
        data=reservation,
        status_code=201,
    )


@reservation_bp.put("/<int:reservation_id>")
def update_reservation(reservation_id):
    """
    Atualiza uma reserva existente.
    """

    current_user = require_auth()

    payload = request.get_json(silent=True) or {}
    data = UpdateReservationSchema.validate(payload)

    reservation_service = get_reservation_service(current_user=current_user)
    reservation = reservation_service.update_reservation(
        reservation_id=reservation_id,
        data=data,
    )

    return success_response(
        data=reservation,
        status_code=200,
    )


@reservation_bp.patch("/<int:reservation_id>/cancel")
def cancel_reservation(reservation_id):
    """
    Cancela uma reserva sem apagar o histórico.
    """

    current_user = require_auth()

    reservation_service = get_reservation_service(current_user=current_user)
    reservation = reservation_service.cancel_reservation(reservation_id)

    return success_response(
        data=reservation,
        status_code=200,
    )