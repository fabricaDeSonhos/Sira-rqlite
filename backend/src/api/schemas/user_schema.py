"""
Schemas de usuários.

Valida criação, atualização e filtros de usuários.
"""

from api.schemas import (
    require_fields,
    normalize_string,
    validate_email,
    validate_choice,
    parse_bool,
    ValidationError,
)


USER_ROLES = (
    "common",
    "admin",
)


class CreateUserSchema:
    """
    Valida criação de usuário.

    Esperado:
    {
        "name": "Gabriel",
        "email": "gabriel@email.com",
        "password": "senha123",
        "role": "common"
    }
    """

    @staticmethod
    def validate(data):
        require_fields(data, ["name", "email", "password"])

        password = normalize_string(data.get("password"), field="password", required=True)

        if len(password) < 8:
            raise ValidationError(
                "A senha deve ter pelo menos 8 caracteres.",
                field="password",
            )

        role = data.get("role") or "common"

        return {
            "name": normalize_string(data.get("name"), field="name", required=True, max_length=100),
            "email": validate_email(data.get("email")),
            "password": password,
            "role": validate_choice(role, field="role", allowed_values=USER_ROLES, required=True),
            "is_active": True,
        }


class UpdateUserSchema:
    """
    Valida atualização de usuário.

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
                max_length=100,
            )

        if "email" in data:
            validated["email"] = validate_email(data.get("email"))

        if "password" in data:
            password = normalize_string(data.get("password"), field="password", required=True)

            if len(password) < 8:
                raise ValidationError(
                    "A senha deve ter pelo menos 8 caracteres.",
                    field="password",
                )

            validated["password"] = password

        if "role" in data:
            validated["role"] = validate_choice(
                data.get("role"),
                field="role",
                allowed_values=USER_ROLES,
                required=True,
            )

        if "is_active" in data:
            validated["is_active"] = parse_bool(data.get("is_active"), field="is_active")

        return validated


class UserFilterSchema:
    """
    Valida filtros de listagem de usuários.

    Query params possíveis:
    - active=true
    - role=admin
    - search=gabriel
    """

    @staticmethod
    def validate(query_params):
        filters = {}

        if query_params.get("active") is not None:
            filters["active"] = parse_bool(query_params.get("active"), field="active")

        if query_params.get("role"):
            filters["role"] = validate_choice(
                query_params.get("role"),
                field="role",
                allowed_values=USER_ROLES,
                required=True,
            )

        if query_params.get("search"):
            filters["search"] = normalize_string(
                query_params.get("search"),
                field="search",
                max_length=100,
            )

        return filters