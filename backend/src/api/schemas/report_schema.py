"""
Schemas de relatórios.

Valida filtros usados em endpoints de relatórios.
"""

from api.schemas import validate_date, parse_int, validate_choice


REPORT_GROUP_BY_OPTIONS = (
    "day",
    "week",
    "month",
    "room",
    "user",
)


class ReportFilterSchema:
    """
    Valida filtros de relatórios.

    Query params possíveis:
    - start_date=2026-06-01
    - end_date=2026-06-30
    - room_id=1
    - user_id=10
    - group_by=day
    """

    @staticmethod
    def validate(query_params):
        filters = {}

        if query_params.get("start_date"):
            filters["start_date"] = validate_date(
                query_params.get("start_date"),
                field="start_date",
            )

        if query_params.get("end_date"):
            filters["end_date"] = validate_date(
                query_params.get("end_date"),
                field="end_date",
            )

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

        if query_params.get("group_by"):
            filters["group_by"] = validate_choice(
                query_params.get("group_by"),
                field="group_by",
                allowed_values=REPORT_GROUP_BY_OPTIONS,
                required=True,
            )

        return filters