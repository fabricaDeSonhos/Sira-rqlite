from reservas.utils.exceptions import ForbiddenError


def require_admin(user):
    if not user or getattr(user, "role", None) != "admin":
        raise ForbiddenError("Apenas administradores podem acessar este recurso.")

    return Trueresponses.py