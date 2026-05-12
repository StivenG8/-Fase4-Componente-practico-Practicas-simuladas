from main.entidades.entidad_base import Entidad
from main.excepciones.errores import ErrorValidacion

class Cliente(Entidad):
    def __init__(self, identificacion, nombre, correo):
        # Atributos privados (encapsulación)
        self.__identificacion = identificacion
        self.__nombre = nombre
        self.__correo = correo
        self.validar()
    
    # Getters
    def get_identificacion(self): return self.__identificacion
    def get_nombre(self): return self.__nombre
    def get_correo(self): return self.__correo
    
    def validar(self):
        """Validación robusta del cliente."""
        if not self.__identificacion or len(str(self.__identificacion)) < 5:
            raise ErrorValidacion("La identificación debe tener al menos 5 caracteres.")
        if not self.__nombre or not isinstance(self.__nombre, str):
            raise ErrorValidacion("El nombre no puede estar vacío y debe ser texto.")
        if "@" not in self.__correo or "." not in self.__correo:
            raise ErrorValidacion("El correo electrónico tiene un formato inválido.")

    def __str__(self):
        return f"{self.__nombre} (ID: {self.__identificacion})"
