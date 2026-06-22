VALID_CREATE_RESERVATION_PAYLOAD = {
    "room_id": 1,
    "date": "2026-06-15",
    "start_time": "08:00",
    "end_time": "09:00",
    "title": "Aula de Programação",
    "details": "Reserva criada via teste de rota.",
}

INVALID_CREATE_RESERVATION_PAYLOAD_MISSING_TITLE = {
    "room_id": 1,
    "date": "2026-06-15",
    "start_time": "08:00",
    "end_time": "09:00",
}

INVALID_CREATE_RESERVATION_PAYLOAD_INVALID_TIME = {
    "room_id": 1,
    "date": "2026-06-15",
    "start_time": "10:00",
    "end_time": "09:00",
    "title": "Aula com horário inválido",
}

VALID_UPDATE_RESERVATION_PAYLOAD = {
    "room_id": 1,
    "date": "2026-06-16",
    "start_time": "10:00",
    "end_time": "11:00",
    "title": "Aula de Banco de Dados",
    "details": "Reserva editada via teste de rota.",
}

VALID_CANCEL_RESERVATION_PAYLOAD = {
    "canceler_user": "admin@test.local",
    "observation": "Cancelada durante teste de rota.",
}

EXPECTED_SUCCESS_KEY = "success"
EXPECTED_DATA_KEY = "data"
EXPECTED_ERROR_KEY = "error"