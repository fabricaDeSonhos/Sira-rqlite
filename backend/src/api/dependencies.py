from pathlib import Path
import sys


# Permite importar módulos internos da pasta service sem alterar o service atual.
SRC_DIR = Path(__file__).resolve().parents[1]
SERVICE_DIR = SRC_DIR / "service"

if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))


from service.service_reservation import (  # noqa: E402
    cancel_reservation,
    create_reservation,
    edit_reservation,
    get_reservation,
    list_reservations,
)


class StaticReservationService:
    """
    Adapter para o service estático atual de reservas.

    Mantém as rotas desacopladas das funções soltas do service.
    """

    def __init__(self, current_user=None):
        self.current_user = current_user

    def list_reservations(self, filters=None):
        """
        Lista reservas.

        O service atual ainda não usa filtros.
        """

        return list_reservations()

    def list_my_reservations(self):
        """
        Lista reservas do usuário atual.

        Temporariamente usa a listagem estática.
        """

        return list_reservations()

    def get_reservation_by_id(self, reservation_id):
        """
        Busca reserva por ID.
        """

        return get_reservation(reservation_id)

    def create_reservation(self, data):
        """
        Cria reserva.
        """

        return create_reservation(data)

    def update_reservation(self, reservation_id, data):
        """
        Atualiza reserva usando a função de edição atual.
        """

        return edit_reservation(
            reservation_id=reservation_id,
            updated_reservation_data=data,
        )

    def cancel_reservation(self, reservation_id, canceler_user=None, observation=None):
        """
        Cancela reserva.
        """

        canceler = canceler_user or _get_current_user_identifier(self.current_user)
        note = observation or "Cancelamento solicitado pela API."

        return cancel_reservation(
            reservation_id=reservation_id,
            canceler_user=canceler,
            observation=note,
        )


class StaticAuthService:
    """
    Service temporário de autenticação.
    """

    def login(self, email, password):
        """
        Simula login.
        """

        return {
            "access_token": "static-dev-token",
            "token_type": "Bearer",
            "user": {
                "id": 1,
                "name": "Administrador",
                "email": email,
                "role": "admin",
                "is_active": True,
            },
        }

    def logout(self):
        """
        Simula logout.
        """

        return {
            "message": "Logout realizado com sucesso.",
        }

    def register(self, data):
        """
        Simula cadastro.
        """

        return {
            "id": 1,
            "name": data.get("name"),
            "email": data.get("email"),
            "role": data.get("role", "common"),
            "is_active": True,
        }


class StaticRoomService:
    """
    Service temporário de salas.
    """

    def __init__(self, current_user=None):
        self.current_user = current_user

    def list_rooms(self, filters=None):
        """
        Lista salas estáticas.
        """

        return [
            {
                "id": 1,
                "name": "Lab 1",
                "description": "Laboratório de informática",
                "capacity": 30,
                "type": "laboratory",
                "is_active": True,
            },
            {
                "id": 2,
                "name": "Sala 101",
                "description": "Sala de aula",
                "capacity": 40,
                "type": "classroom",
                "is_active": True,
            },
        ]

    def get_room_by_id(self, room_id):
        """
        Busca sala por ID.
        """

        for room in self.list_rooms():
            if room["id"] == room_id:
                return room

        return {
            "result": "error",
            "details": "Sala não encontrada.",
        }

    def create_room(self, data):
        """
        Simula criação de sala.
        """

        return {
            "id": 3,
            **data,
        }

    def update_room(self, room_id, data):
        """
        Simula atualização de sala.
        """

        return {
            "id": room_id,
            **data,
        }

    def deactivate_room(self, room_id):
        """
        Simula desativação de sala.
        """

        return {
            "id": room_id,
            "is_active": False,
        }

    def activate_room(self, room_id):
        """
        Simula ativação de sala.
        """

        return {
            "id": room_id,
            "is_active": True,
        }


class StaticUserService:
    """
    Service temporário de usuários.
    """

    def __init__(self, current_user=None):
        self.current_user = current_user

    def list_users(self, filters=None):
        """
        Lista usuários estáticos.
        """

        return [
            {
                "id": 1,
                "name": "Administrador",
                "email": "admin@sira.local",
                "role": "admin",
                "is_active": True,
            },
            {
                "id": 2,
                "name": "Usuário Comum",
                "email": "user@sira.local",
                "role": "common",
                "is_active": True,
            },
        ]

    def get_user_by_id(self, user_id):
        """
        Busca usuário por ID.
        """

        for user in self.list_users():
            if user["id"] == user_id:
                return user

        return {
            "result": "error",
            "details": "Usuário não encontrado.",
        }

    def create_user(self, data):
        """
        Simula criação de usuário.
        """

        return {
            "id": 3,
            **data,
        }

    def update_user(self, user_id, data):
        """
        Simula atualização de usuário.
        """

        return {
            "id": user_id,
            **data,
        }

    def deactivate_user(self, user_id):
        """
        Simula desativação de usuário.
        """

        return {
            "id": user_id,
            "is_active": False,
        }

    def activate_user(self, user_id):
        """
        Simula ativação de usuário.
        """

        return {
            "id": user_id,
            "is_active": True,
        }


class StaticReportService:
    """
    Service temporário de relatórios.
    """

    def __init__(self, current_user=None):
        self.current_user = current_user

    def get_summary(self, filters=None):
        """
        Retorna resumo estático.
        """

        return {
            "total_reservations": 2,
            "active_reservations": 2,
            "cancelled_reservations": 0,
            "total_rooms": 2,
            "total_users": 2,
        }

    def get_reservations_by_room(self, filters=None):
        """
        Retorna reservas por sala.
        """

        return [
            {
                "room_id": 1,
                "room_name": "Lab 1",
                "total_reservations": 1,
            },
            {
                "room_id": 2,
                "room_name": "Sala 101",
                "total_reservations": 1,
            },
        ]

    def get_room_usage(self, filters=None):
        """
        Retorna uso das salas.
        """

        return [
            {
                "room_id": 1,
                "room_name": "Lab 1",
                "usage_percent": 45,
            },
            {
                "room_id": 2,
                "room_name": "Sala 101",
                "usage_percent": 30,
            },
        ]

    def get_reservations_by_user(self, filters=None):
        """
        Retorna reservas por usuário.
        """

        return [
            {
                "user_id": 1,
                "user_name": "Administrador",
                "total_reservations": 1,
            },
            {
                "user_id": 2,
                "user_name": "Usuário Comum",
                "total_reservations": 1,
            },
        ]


def get_current_user():
    """
    Retorna usuário atual temporário.

    Futuramente deve validar JWT.
    """

    return {
        "id": 1,
        "name": "Administrador",
        "email": "admin@sira.local",
        "role": "admin",
        "is_active": True,
    }


def get_auth_service():
    """
    Retorna service de autenticação.
    """

    return StaticAuthService()


def get_room_service(current_user=None):
    """
    Retorna service de salas.
    """

    return StaticRoomService(current_user=current_user)


def get_reservation_service(current_user=None):
    """
    Retorna service de reservas.
    """

    return StaticReservationService(current_user=current_user)


def get_user_service(current_user=None):
    """
    Retorna service de usuários.
    """

    return StaticUserService(current_user=current_user)


def get_report_service(current_user=None):
    """
    Retorna service de relatórios.
    """

    return StaticReportService(current_user=current_user)


def _get_current_user_identifier(current_user):
    """
    Extrai identificador simples do usuário atual.
    """

    if not current_user:
        return "system"

    return (
        current_user.get("email")
        or current_user.get("name")
        or str(current_user.get("id"))
        or "system"
    )