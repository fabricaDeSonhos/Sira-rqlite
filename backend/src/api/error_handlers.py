from api.responses import error_response
from api.schemas import ValidationError


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return error_response(
            message=error.message,
            code=error.code,
            status_code=400,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        return error_response(
            message="Erro interno do servidor.",
            code="INTERNAL_SERVER_ERROR",
            status_code=500,
        )