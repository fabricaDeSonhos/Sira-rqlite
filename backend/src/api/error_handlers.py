from flask import Flask

from api.responses import error_response
from api.schemas import ValidationError


class ApiError(Exception):
    """
    Erro base da API.

    Use esta classe para criar erros com status HTTP controlado.
    """

    status_code = 400
    code = "API_ERROR"

    def __init__(self, message="Erro na requisição.", status_code=None, code=None):
        super().__init__(message)
        self.message = message

        if status_code is not None:
            self.status_code = status_code

        if code is not None:
            self.code = code


class UnauthorizedError(ApiError):
    """
    Erro para usuário não autenticado.
    """

    status_code = 401
    code = "UNAUTHORIZED"


class ForbiddenError(ApiError):
    """
    Erro para usuário sem permissão.
    """

    status_code = 403
    code = "FORBIDDEN"


class NotFoundError(ApiError):
    """
    Erro para recurso não encontrado.
    """

    status_code = 404
    code = "NOT_FOUND"


class ConflictError(ApiError):
    """
    Erro para conflito de regra de negócio.
    Exemplo: sala já reservada no horário informado.
    """

    status_code = 409
    code = "CONFLICT"


def register_error_handlers(app: Flask):
    """
    Registra os tratadores globais de erro no app Flask.
    """

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """
        Trata erros gerados pelos schemas.
        """

        return error_response(
            message=getattr(error, "message", str(error)),
            code=getattr(error, "code", "VALIDATION_ERROR"),
            status_code=400,
        )

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        """
        Trata erros controlados da API.
        """

        return error_response(
            message=error.message,
            code=error.code,
            status_code=error.status_code,
        )

    @app.errorhandler(404)
    def handle_route_not_found(error):
        """
        Trata rotas inexistentes.
        """

        return error_response(
            message="Rota não encontrada.",
            code="ROUTE_NOT_FOUND",
            status_code=404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """
        Trata método HTTP inválido para a rota.
        """

        return error_response(
            message="Método HTTP não permitido para esta rota.",
            code="METHOD_NOT_ALLOWED",
            status_code=405,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """
        Trata erros inesperados.

        Em produção, registre o erro em logs.
        """

        return error_response(
            message="Erro interno do servidor.",
            code="INTERNAL_SERVER_ERROR",
            status_code=500,
        )