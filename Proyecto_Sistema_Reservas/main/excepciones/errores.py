"""Excepciones personalizadas para el dominio del sistema."""

class ErrorValidacion(Exception):
    """Excepción para errores de validación de datos."""
    pass

class ErrorReserva(Exception):
    """Excepción para errores lógicos al crear o procesar una reserva."""
    pass
