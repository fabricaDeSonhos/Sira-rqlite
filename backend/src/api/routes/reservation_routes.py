from flask import Blueprint, request

from api.responses import success_response, error_response
from api.schemas.reservation_schema import (
    CreateReservationSchema,
    UpdateReservationSchema,
)
from service.service_reservation import (
    cancel_reservation as service_cancel_reservation,
    create_reservation as service_create_reservation,
    edit_reservation as service_edit_reservation,
    get_reservation as service_get_reservation,
    list_reservations as service_list_reservations,
)


reservation_bp = Blueprint("reservations", __name__)


def _service_result_to_response(service_result, success_status_code=200, error_status_code=400):
    """
    Converte o padrão atual do service em resposta HTTP.

    Esperado do service:
    {
        "result": "ok" | "error",
        "details": ...
    }
    """

    if not isinstance(service_result, dict):
        return error_response(
            message="Resposta inválida do service.",
            code="INVALID_SERVICE_RESPONSE",
            status_code=500,
        )

    result = service_result.get("result")
    details = service_result.get("details")

    if result == "ok":
        return success_response(
            data=details,
            status_code=success_status_code,
        )

    return error_response(
        message=details or "Erro ao processar reserva.",
        code="RESERVATION_SERVICE_ERROR",
        status_code=error_status_code,
    )


@reservation_bp.get("")
def list_reservations():
    """
    Lista reservas.

    Atualmente usa dados estáticos do service.
    """

    service_result = service_list_reservations()

    return _service_result_to_response(
        service_result,
        success_status_code=200,
    )


@reservation_bp.get("/<int:reservation_id>")
def get_reservation(reservation_id):
    """
    Busca uma reserva pelo ID.
    """

    service_result = service_get_reservation(reservation_id)

    error_status_code = 404
    if service_result.get("result") == "error":
        error_status_code = 404

    return _service_result_to_response(
        service_result,
        success_status_code=200,
        error_status_code=error_status_code,
    )


@reservation_bp.post("")
def create_reservation():
    """
    Cria uma nova reserva.

    O schema valida a entrada antes de chamar o service.
    """

    payload = request.get_json(silent=True) or {}
    data = CreateReservationSchema.validate(payload)

    service_result = service_create_reservation(data)

    return _service_result_to_response(
        service_result,
        success_status_code=201,
        error_status_code=400,
    )


@reservation_bp.put("/<int:reservation_id>")
def update_reservation(reservation_id):
    """
    Edita uma reserva existente.

    O service atual implementa edição como:
    cancelar reserva antiga + criar nova reserva.
    """

    payload = request.get_json(silent=True) or {}
    data = UpdateReservationSchema.validate(payload)

    service_result = service_edit_reservation(
        reservation_id=reservation_id,
        updated_reservation_data=data,
    )

    return _service_result_to_response(
        service_result,
        success_status_code=200,
        error_status_code=404,
    )


@reservation_bp.patch("/<int:reservation_id>/cancel")
def cancel_reservation(reservation_id):
    """
    Cancela uma reserva sem apagar histórico.
    """

    payload = request.get_json(silent=True) or {}

    canceler_user = payload.get("canceler_user") or "system"
    observation = payload.get("observation") or "Cancelamento solicitado pela API."

    service_result = service_cancel_reservation(
        reservation_id=reservation_id,
        canceler_user=canceler_user,
        observation=observation,
    )

    return _service_result_to_response(
        service_result,
        success_status_code=200,
        error_status_code=404,
    )