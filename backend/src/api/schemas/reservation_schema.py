"""
Schemas de reservas.

Valida criação, atualização e filtros de reservas.

Cuidados importantes:
- user_id não deve vir do front para criar reserva comum.
- o usuário deve vir da autenticação.
- datas devem seguir YYYY-MM-DD.
- horários devem seguir HH:MM.
"""

from api.schemas import (
    require_fields,
    normalize_string,
    parse_int,
    validate_date,
    validate_time,
    ensure_time_range,
    validate_choice,
)


RESERVATION_STATUSES = (
    "active",
    "cancelled",
    "completed",
    "fixed",
)


class CreateReservationSchema:
    """
    Valida criação de reserva.

    Esperado:
    {
        "room_id": 1,
        "date": "2026-06-12",
        "start_time": "08:00",
        "end_time": "09:00",
        "title": "Aula de Programação",
        "details": "Opcional"
    }
    """

    @staticmethod
    def validate(data):
        require_fields(data, ["room_id", "date", "start_time", "end_time", "title"])

        start_time = validate_time(data.get("start_time"), field="start_time")
        end_time = validate_time(data.get("end_time"), field="end_time")

        ensure_time_range(start_time, end_time)

        return {
            "room_id": parse_int(data.get("room_id"), field="room_id", required=True, min_value=1),
            "date": validate_date(data.get("date"), field="date"),
            "start_time": start_time,
            "end_time": end_time,
            "title": normalize_string(data.get("title"), field="title", required=True, max_length=120),
            "details": normalize_string(data.get("details"), field="details", max_length=300),
            "status": "active",
        }


class UpdateReservationSchema:
    """
    Valida atualização de reserva.

    Todos os campos são opcionais.
    Se start_time e end_time vierem juntos, valida o intervalo.
    """

    @staticmethod
    def validate(data):
        validated = {}

        if "room_id" in data:
            validated["room_id"] = parse_int(
                data.get("room_id"),
                field="room_id",
                required=True,
                min_value=1,
            )

        if "date" in data:
            validated["date"] = validate_date(data.get("date"), field="date")

        if "start_time" in data:
            validated["start_time"] = validate_time(data.get("start_time"), field="start_time")

        if "end_time" in data:
            validated["end_time"] = validate_time(data.get("end_time"), field="end_time")

        if "start_time" in validated and "end_time" in validated:
            ensure_time_range(validated["start_time"], validated["end_time"])

        if "title" in data:
            validated["title"] = normalize_string(
                data.get("title"),
                field="title",
                required=True,
                max_length=120,
            )

        if "details" in data:
            validated["details"] = normalize_string(
                data.get("details"),
                field="details",
                max_length=300,
            )

        if "status" in data:
            validated["status"] = validate_choice(
                data.get("status"),
                field="status",
                allowed_values=RESERVATION_STATUSES,
                required=True,
            )

        return validated


class ReservationFilterSchema:
    """
    Valida filtros de listagem de reservas.

    Query params possíveis:
    - date=2026-06-12
    - start_date=2026-06-01
    - end_date=2026-06-30
    - room_id=1
    - user_id=10
    - status=active
    """

    @staticmethod
    def validate(query_params):
        filters = {}

        if query_params.get("date"):
            filters["date"] = validate_date(query_params.get("date"), field="date")

        if query_params.get("start_date"):
            filters["start_date"] = validate_date(query_params.get("start_date"), field="start_date")

        if query_params.get("end_date"):
            filters["end_date"] = validate_date(query_params.get("end_date"), field="end_date")

        if query_params.get("room_id"):
            filters["room_id"] = parse_int(
                query_params.get("room_id"),
                field="room_id",
                min_value=1,
            )

        if query_params.get("user_id"):
            filters["user_id"] = parse_int(
                query_params.get("user_id"),
                field="user_id",
                min_value=1,
            )

        if query_params.get("status"):
            filters["status"] = validate_choice(
                query_params.get("status"),
                field="status",
                allowed_values=RESERVATION_STATUSES,
                required=True,
            )

        return filters