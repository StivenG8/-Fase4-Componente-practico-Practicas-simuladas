from abc import ABC, abstractmethod
from main.entidades.entidad_base import Entidad
from main.excepciones.errores import ErrorValidacion

class Servicio(Entidad, ABC):
    """Clase abstracta de servicio."""
    def __init__(self, id_servicio, nombre, costo_base):
        self._id_servicio = id_servicio
        self._nombre = nombre
        self._costo_base = costo_base
        self.validar()
        
    def get_nombre(self):
        return self._nombre
    
    def get_id(self):
        return self._id_servicio

    def validar(self):
        if self._costo_base <= 0:
            raise ErrorValidacion("El costo base del servicio debe ser mayor a 0.")
            
    @abstractmethod
    def calcular_costo(self, cantidad, descuento=0.0, impuesto=0.0):
        """
        Método sobrecargado (vía parámetros opcionales en Python).
        """
        pass

    def __str__(self):
        return f"{self._nombre} (ID: {self._id_servicio})"
