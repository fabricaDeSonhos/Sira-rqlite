"""
Schemas de salas.

Valida criação, atualização e filtros de salas.
"""

from api.schemas import (
    require_fields,
    normalize_string,
    parse_int,
    parse_bool,
    validate_choice,
)


ROOM_TYPES = (
    "classroom",
    "laboratory",
    "auditorium",
    "meeting_room",
)


class CreateRoomSchema:
    """
    Valida criação de sala.

    Esperado:
    {
        "name": "Lab 1",
        "description": "Laboratório de informática",
        "capacity": 30,
        "type": "laboratory",
        "floor": "Bloco A",
        "resources": ["projector", "wifi"]
    }
    """

    @staticmethod
    def validate(data):
        require_fields(data, ["name", "capacity"])

        resources = data.get("resources", [])

        if resources is None:
            resources = []

        if not isinstance(resources, list):
            resources = []

        return {
            "name": normalize_string(data.get("name"), field="name", required=True, max_length=80),
            "description": normalize_string(data.get("description"), field="description", max_length=255),
            "capacity": parse_int(data.get("capacity"), field="capacity", required=True, min_value=1),
            "type": validate_choice(
                data.get("type") or "classroom",
                field="type",
                allowed_values=ROOM_TYPES,
                required=True,
            ),
            "floor": normalize_string(data.get("floor"), field="floor", max_length=80),
            "resources": resources,
            "is_active": True,
        }


class UpdateRoomSchema:
    """
    Valida atualização de sala.

    Todos os campos são opcionais.
    """

    @staticmethod
    def validate(data):
        validated = {}

        if "name" in data:
            validated["name"] = normalize_string(
                data.get("name"),
                field="name",
                required=True,
                max_length=80,
            )

        if "description" in data:
            validated["description"] = normalize_string(
                data.get("description"),
                field="description",
                max_length=255,
            )

        if "capacity" in data:
            validated["capacity"] = parse_int(
                data.get("capacity"),
                field="capacity",
                required=True,
                min_value=1,
            )

        if "type" in data:
            validated["type"] = validate_choice(
                data.get("type"),
                field="type",
                allowed_values=ROOM_TYPES,
                required=True,
            )

        if "floor" in data:
            validated["floor"] = normalize_string(
                data.get("floor"),
                field="floor",
                max_length=80,
            )

        if "resources" in data:
            resources = data.get("resources")

            if not isinstance(resources, list):
                resources = []

            validated["resources"] = resources

        if "is_active" in data:
            validated["is_active"] = parse_bool(data.get("is_active"), field="is_active")

        return validated


class RoomFilterSchema:
    """
    Valida filtros de listagem de salas.

    Query params possíveis:
    - active=true
    - search=lab
    - type=laboratory
    """

    @staticmethod
    def validate(query_params):
        return {
            "active": parse_bool(query_params.get("active"), field="active", default=None),
            "search": normalize_string(query_params.get("search"), field="search", max_length=80),
            "type": validate_choice(
                query_params.get("type"),
                field="type",
                allowed_values=ROOM_TYPES,
                required=False,
            ),
        }