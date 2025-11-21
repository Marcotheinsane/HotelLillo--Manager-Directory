from django.core.exceptions import ValidationError
import re


def _normalize_rut(rut: str) -> str:
    if not isinstance(rut, str):
        raise ValidationError("RUT inválido")
    r = rut.upper().replace('.', '').replace(' ', '')
    # If user provided digits+dv without hyphen, insert it
    if '-' not in r and len(r) > 1:
        r = r[:-1] + '-' + r[-1]
    return r


def validar_rut(value: str):
    """Valida un RUT chileno básico. Levanta ValidationError si es inválido.

    Acepta formatos con o sin puntos, con o sin guión. No hace transformaciones
    permanentes, sólo valida.
    """
    if value is None or str(value).strip() == '':
        raise ValidationError("El RUT es obligatorio.")

    try:
        rut = _normalize_rut(value)
    except ValidationError:
        raise ValidationError("Formato de RUT inválido.")

    match = re.match(r'^(\d{1,8})-([0-9K])$', rut)
    if not match:
        raise ValidationError("Formato de RUT inválido. Ej: 12345678-9")

    numeros, dv = match.groups()

    reversed_digits = map(int, reversed(numeros))
    factors = [2, 3, 4, 5, 6, 7]
    s = 0
    i = 0
    for d in reversed_digits:
        s += d * factors[i % len(factors)]
        i += 1

    res = 11 - (s % 11)
    if res == 11:
        expected = '0'
    elif res == 10:
        expected = 'K'
    else:
        expected = str(res)

    if dv != expected:
        raise ValidationError('RUT inválido.')


def validar_telefono(value: str):
    if value is None or str(value).strip() == '':
        # allow blank, other validators may enforce required
        return
    v = str(value).strip()
    cleaned = v.replace('+', '').replace(' ', '').replace('-', '')
    if not cleaned.isdigit():
        raise ValidationError('Teléfono inválido: sólo números, +, - y espacios permitidos.')
    if not 6 <= len(cleaned) <= 15:
        raise ValidationError('Teléfono inválido: largo debe ser entre 6 y 15 dígitos.')
