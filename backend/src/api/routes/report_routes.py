"""
Rotas de relatórios.
"""

from flask import Blueprint, request

from api.dependencies import get_report_service
from api.guards.admin_guard import require_admin
from api.guards.auth_guard import require_auth
from api.responses import success_response
from api.schemas.report_schema import ReportFilterSchema


report_bp = Blueprint("reports", __name__)


@report_bp.get("/summary")
def summary():
    """
    Retorna resumo geral do sistema.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    filters = ReportFilterSchema.validate(request.args.to_dict())

    report_service = get_report_service(current_user=current_user)
    report = report_service.get_summary(filters=filters)

    return success_response(
        data=report,
        status_code=200,
    )


@report_bp.get("/reservations-by-room")
def reservations_by_room():
    """
    Retorna reservas agrupadas por sala.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    filters = ReportFilterSchema.validate(request.args.to_dict())

    report_service = get_report_service(current_user=current_user)
    report = report_service.get_reservations_by_room(filters=filters)

    return success_response(
        data=report,
        status_code=200,
    )


@report_bp.get("/room-usage")
def room_usage():
    """
    Retorna uso das salas por período.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    filters = ReportFilterSchema.validate(request.args.to_dict())

    report_service = get_report_service(current_user=current_user)
    report = report_service.get_room_usage(filters=filters)

    return success_response(
        data=report,
        status_code=200,
    )


@report_bp.get("/reservations-by-user")
def reservations_by_user():
    """
    Retorna reservas agrupadas por usuário.

    Requer administrador.
    """

    current_user = require_auth()
    require_admin(current_user)

    filters = ReportFilterSchema.validate(request.args.to_dict())

    report_service = get_report_service(current_user=current_user)
    report = report_service.get_reservations_by_user(filters=filters)

    return success_response(
        data=report,
        status_code=200,
    )