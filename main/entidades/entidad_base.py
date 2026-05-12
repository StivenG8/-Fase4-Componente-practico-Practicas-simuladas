from abc import ABC, abstractmethod

class Entidad(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    @abstractmethod
    def validar(self):
        """Método abstracto para validar el estado de la entidad."""
        pass
