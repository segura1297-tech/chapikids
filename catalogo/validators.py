from django.core.exceptions import ValidationError
import re


def validar_telefono_mexicano(valor):
    """Valida que el teléfono sea de 10 dígitos (México)."""
    # Remover espacios, guiones, paréntesis
    limpio = re.sub(r'[\s\-\(\)]', '', valor)

    # Debe ser exactamente 10 dígitos
    if not re.match(r'^\d{10}$', limpio):
        raise ValidationError('El teléfono debe tener 10 dígitos (México).')


def validar_fecha_futura(valor):
    """Valida que la fecha del evento sea futura."""
    from datetime import date
    if valor < date.today():
        raise ValidationError('La fecha del evento debe ser futura.')


def validar_precio_positivo(valor):
    """Valida que el precio sea positivo."""
    if valor <= 0:
        raise ValidationError('El precio debe ser mayor a cero.')
