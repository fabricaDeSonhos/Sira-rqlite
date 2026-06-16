
from api.error_handlers import ForbiddenError


def require_admin(user):
    """
    Exige usuário administrador.
    """

    if not user:
        raise ForbiddenError("Usuário não autenticado.")

    if user.get("role") != "admin":
        raise ForbiddenError("Apenas administradores podem acessar este recurso.")

    return True