"""
Schemas de autenticação.

Responsáveis por validar payloads de login, cadastro e refresh de token.
"""

from api.schemas import require_fields, validate_email, normalize_string, ValidationError


class LoginSchema:
    """
    Valida o payload de login.

    Esperado:
    {
        "email": "usuario@email.com",
        "password": "senha"
    }
    """

    @staticmethod
    def validate(data):
        require_fields(data, ["email", "password"])

        return {
            "email": validate_email(data.get("email")),
            "password": normalize_string(
                data.get("password"),
                field="password",
                required=True,
            ),
        }


class RegisterSchema:
    """
    Valida payload de cadastro.

    Pode ser usado se o sistema permitir cadastro público.
    Se o cadastro for apenas por admin, você pode usar CreateUserSchema.
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

        return {
            "name": normalize_string(data.get("name"), field="name", required=True, max_length=100),
            "email": validate_email(data.get("email")),
            "password": password,
        }


class RefreshTokenSchema:
    """
    Valida payload para renovação de token.

    Opcional, caso você implemente refresh token.
    """

    @staticmethod
    def validate(data):
        require_fields(data, ["refresh_token"])

        return {
            "refresh_token": normalize_string(
                data.get("refresh_token"),
                field="refresh_token",
                required=True,
            )
        }