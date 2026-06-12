"""
Dependências compartilhadas pelas rotas.

No começo, este arquivo pode montar services diretamente.
Depois, você pode evoluir para injeção de dependência mais robusta.
"""

from reservas.services.auth_service import AuthService
from reservas.services.room_service import RoomService
from reservas.services.reservation_service import ReservationService
from reservas.services.user_service import UserService
from reservas.services.report_service import ReportService


def get_current_user():
    """
    Retorna o usuário autenticado.

    Implementação temporária:
    - No começo, pode retornar um usuário fake.
    - Depois, deve ler o token JWT da requisição.
    """

    # TODO: trocar por autenticação real com JWT.
    return None


def get_auth_service():
    return AuthService()


def get_room_service(current_user=None):
    return RoomService(current_user=current_user)


def get_reservation_service(current_user=None):
    return ReservationService(current_user=current_user)


def get_user_service(current_user=None):
    return UserService(current_user=current_user)


def get_report_service(current_user=None):
    return ReportService(current_user=current_user)