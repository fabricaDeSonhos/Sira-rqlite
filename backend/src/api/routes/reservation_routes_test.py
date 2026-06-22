import pytest
from flask import Flask

from api.routes.reservation_routes import reservation_bp
from api.routes.reservation_routes_static_data import (
    EXPECTED_DATA_KEY,
    EXPECTED_ERROR_KEY,
    EXPECTED_SUCCESS_KEY,
    INVALID_CREATE_RESERVATION_PAYLOAD_INVALID_TIME,
    INVALID_CREATE_RESERVATION_PAYLOAD_MISSING_TITLE,
    VALID_CANCEL_RESERVATION_PAYLOAD,
    VALID_CREATE_RESERVATION_PAYLOAD,
    VALID_UPDATE_RESERVATION_PAYLOAD,
)


@pytest.fixture()
def app():
    """
    Cria uma aplicação Flask mínima para testar o blueprint.
    """

    test_app = Flask(__name__)
    test_app.register_blueprint(reservation_bp, url_prefix="/api/reservations")
    test_app.config.update(TESTING=True)

    return test_app


@pytest.fixture()
def client(app):
    """
    Cria o client HTTP de testes.
    """

    return app.test_client()


def test_list_reservations_should_return_success(client):
    """
    Deve listar reservas usando o service estático.
    """

    response = client.get("/api/reservations")
    body = response.get_json()

    assert response.status_code == 200
    assert body[EXPECTED_SUCCESS_KEY] is True
    assert EXPECTED_DATA_KEY in body


def test_get_existing_reservation_should_return_success(client):
    """
    Deve buscar uma reserva existente.
    """

    response = client.get("/api/reservations/1")
    body = response.get_json()

    assert response.status_code == 200
    assert body[EXPECTED_SUCCESS_KEY] is True
    assert EXPECTED_DATA_KEY in body


def test_get_missing_reservation_should_return_error(client):
    """
    Deve retornar erro ao buscar reserva inexistente.
    """

    response = client.get("/api/reservations/999")
    body = response.get_json()

    assert response.status_code == 404
    assert body[EXPECTED_SUCCESS_KEY] is False
    assert EXPECTED_ERROR_KEY in body


def test_create_reservation_should_return_created(client):
    """
    Deve criar reserva com payload válido.
    """

    response = client.post(
        "/api/reservations",
        json=VALID_CREATE_RESERVATION_PAYLOAD,
    )
    body = response.get_json()

    assert response.status_code == 201
    assert body[EXPECTED_SUCCESS_KEY] is True
    assert EXPECTED_DATA_KEY in body


def test_create_reservation_missing_title_should_return_validation_error(client):
    """
    Deve rejeitar criação sem título.
    """

    response = client.post(
        "/api/reservations",
        json=INVALID_CREATE_RESERVATION_PAYLOAD_MISSING_TITLE,
    )
    body = response.get_json()

    assert response.status_code == 400
    assert body[EXPECTED_SUCCESS_KEY] is False
    assert EXPECTED_ERROR_KEY in body


def test_create_reservation_invalid_time_should_return_validation_error(client):
    """
    Deve rejeitar horário final menor que inicial.
    """

    response = client.post(
        "/api/reservations",
        json=INVALID_CREATE_RESERVATION_PAYLOAD_INVALID_TIME,
    )
    body = response.get_json()

    assert response.status_code == 400
    assert body[EXPECTED_SUCCESS_KEY] is False
    assert EXPECTED_ERROR_KEY in body


def test_update_reservation_should_return_success(client):
    """
    Deve editar reserva existente.
    """

    response = client.put(
        "/api/reservations/1",
        json=VALID_UPDATE_RESERVATION_PAYLOAD,
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body[EXPECTED_SUCCESS_KEY] is True
    assert EXPECTED_DATA_KEY in body


def test_cancel_reservation_should_return_success(client):
    """
    Deve cancelar reserva existente.
    """

    response = client.patch(
        "/api/reservations/1/cancel",
        json=VALID_CANCEL_RESERVATION_PAYLOAD,
    )
    body = response.get_json()

    assert response.status_code == 200
    assert body[EXPECTED_SUCCESS_KEY] is True
    assert EXPECTED_DATA_KEY in body


def test_cancel_missing_reservation_should_return_error(client):
    """
    Deve retornar erro ao cancelar reserva inexistente.
    """

    response = client.patch(
        "/api/reservations/999/cancel",
        json=VALID_CANCEL_RESERVATION_PAYLOAD,
    )
    body = response.get_json()

    assert response.status_code == 404
    assert body[EXPECTED_SUCCESS_KEY] is False
    assert EXPECTED_ERROR_KEY in body