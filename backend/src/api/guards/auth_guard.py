from reservas.api.dependencies import get_current_user
from reservas.utils.exceptions import UnauthorizedError


def require_auth():
    current_user = get_current_user()

    if not current_user:
        raise UnauthorizedError("Autenticação obrigatória.")

    return current_user