"""
Utilitários compartilhados pelos schemas da API.

Schemas validam e normalizam dados recebidos nas requisições HTTP.
Eles não devem acessar banco de dados e não devem conter regra de negócio pesada.
"""

from datetime import datetime
import re


class ValidationError(Exception):
    """
    Erro lançado quando o payload enviado para a API é inválido.

    O error_handlers.py pode capturar essa exceção e transformar em HTTP 400.
    """

    def __init__(self, message, field=None, code="VALIDATION_ERROR"):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require_fields(data, required_fields):
    """
    Garante que todos os campos obrigatórios existem e não estão vazios.
    """

    if not isinstance(data, dict):
        raise ValidationError("O corpo da requisição deve ser um JSON válido.")

    missing_fields = []

    for field in required_fields:
        value = data.get(field)

        if value is None:
            missing_fields.append(field)
        elif isinstance(value, str) and not value.strip():
            missing_fields.append(field)

    if missing_fields:
        fields = ", ".join(missing_fields)
        raise ValidationError(
            message=f"Campos obrigatórios ausentes ou vazios: {fields}.",
            field=missing_fields[0],
        )


def normalize_string(value, field, required=False, max_length=None):
    """
    Normaliza strings removendo espaços extras.
    """

    if value is None:
        if required:
            raise ValidationError(f"O campo '{field}' é obrigatório.", field=field)
        return None

    if not isinstance(value, str):
        raise ValidationError(f"O campo '{field}' deve ser um texto.", field=field)

    normalized = value.strip()

    if required and not normalized:
        raise ValidationError(f"O campo '{field}' não pode ser vazio.", field=field)

    if max_length is not None and len(normalized) > max_length:
        raise ValidationError(
            f"O campo '{field}' deve ter no máximo {max_length} caracteres.",
            field=field,
        )

    return normalized


def parse_int(value, field, required=False, min_value=None):
    """
    Converte valor para inteiro e valida limite mínimo.
    """

    if value is None:
        if required:
            raise ValidationError(f"O campo '{field}' é obrigatório.", field=field)
        return None

    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"O campo '{field}' deve ser um número inteiro.", field=field)

    if min_value is not None and parsed < min_value:
        raise ValidationError(
            f"O campo '{field}' deve ser maior ou igual a {min_value}.",
            field=field,
        )

    return parsed


def parse_bool(value, field, default=None):
    """
    Converte valores comuns para boolean.

    Aceita:
    - true, false
    - "true", "false"
    - "1", "0"
    - 1, 0
    """

    if value is None:
        return default

    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        if value == 1:
            return True
        if value == 0:
            return False

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in ("true", "1", "yes", "sim"):
            return True

        if normalized in ("false", "0", "no", "nao", "não"):
            return False

    raise ValidationError(f"O campo '{field}' deve ser booleano.", field=field)


def validate_email(value, field="email"):
    """
    Valida formato básico de e-mail.
    """

    email = normalize_string(value, field=field, required=True, max_length=255)

    if not EMAIL_PATTERN.match(email):
        raise ValidationError("Formato de e-mail inválido.", field=field)

    return email.lower()


def validate_date(value, field="date"):
    """
    Valida data no formato YYYY-MM-DD.

    Retorna a string normalizada, não um objeto date, para facilitar uso com rqlite.
    """

    date_text = normalize_string(value, field=field, required=True)

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(
            f"O campo '{field}' deve estar no formato YYYY-MM-DD.",
            field=field,
        )

    return date_text


def validate_time(value, field):
    """
    Valida horário no formato HH:MM.

    Retorna string normalizada.
    """

    time_text = normalize_string(value, field=field, required=True)

    try:
        datetime.strptime(time_text, "%H:%M")
    except ValueError:
        raise ValidationError(
            f"O campo '{field}' deve estar no formato HH:MM.",
            field=field,
        )

    return time_text


def time_to_minutes(time_text):
    """
    Converte HH:MM para minutos.
    """

    hours, minutes = time_text.split(":")
    return int(hours) * 60 + int(minutes)


def ensure_time_range(start_time, end_time):
    """
    Garante que o horário final é depois do horário inicial.
    """

    if time_to_minutes(end_time) <= time_to_minutes(start_time):
        raise ValidationError(
            "O horário de término deve ser depois do horário de início.",
            field="end_time",
        )


def validate_choice(value, field, allowed_values, required=False):
    """
    Valida se um valor está dentro de uma lista permitida.
    """

    normalized = normalize_string(value, field=field, required=required)

    if normalized is None:
        return None

    if normalized not in allowed_values:
        allowed = ", ".join(allowed_values)
        raise ValidationError(
            f"O campo '{field}' deve ser um destes valores: {allowed}.",
            field=field,
        )

    return normalized