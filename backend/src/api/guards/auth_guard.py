from api.dependencies import get_current_user
from api.error_handlers import UnauthorizedError


def require_auth():
    """
    Exige usuário autenticado.
    """

    current_user = get_current_user()

    if not current_user:
        raise UnauthorizedError("Autenticação obrigatória.")

    return current_user