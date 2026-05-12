import logging
from main.excepciones.errores import ErrorValidacion, ErrorReserva

class Reserva:
    def __init__(self, id_reserva, cliente, servicio, cantidad_tiempo):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.cantidad_tiempo = cantidad_tiempo
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def procesar_reserva(self, descuento=0.0, impuesto=0.0):
        """
        Procesa la reserva demostrando uso avanzado de bloques try.
        """
        logging.info(f"Iniciando procesamiento de reserva {self.id_reserva}")
        
        try:
            # Validación de lógicas de negocio
            if self.cantidad_tiempo <= 0:
                raise ErrorValidacion("La cantidad de tiempo debe ser mayor a 0.")
            if self.estado == "Cancelada":
                raise ErrorReserva("No se puede procesar una reserva cancelada.")
                
            # Polimorfismo y sobrecarga
            self.costo_total = self.servicio.calcular_costo(
                self.cantidad_tiempo, descuento, impuesto
            )
            
            if self.costo_total < 0:
                raise ValueError("El cálculo resultó en un costo negativo.")
                
        except ErrorValidacion as ev:
            # Encadenamiento de excepciones
            logging.error(f"Falla de validación en reserva {self.id_reserva}: {ev}")
            self.estado = "Fallida"
            raise ErrorReserva(f"Reserva fallida por validación: {ev}") from ev
            
        except ValueError as ve:
            logging.error(f"Error de cálculo en reserva {self.id_reserva}: {ve}")
            self.estado = "Fallida"
            raise ErrorReserva(f"Reserva fallida por error matemático: {ve}") from ve
            
        else:
            self.estado = "Confirmada"
            logging.info(f"Reserva {self.id_reserva} procesada exitosamente. Costo: ${self.costo_total:.2f}")
            
        finally:
            logging.info(f"Finalizó el intento de procesamiento de la reserva {self.id_reserva}. Estado actual: {self.estado}")

    def cancelar(self):
        self.estado = "Cancelada"
        logging.info(f"Reserva {self.id_reserva} ha sido cancelada.")

    def __str__(self):
        return f"{self.id_reserva} - {self.cliente.get_nombre()} - {self.servicio.get_nombre()} - {self.cantidad_tiempo}h - {self.estado}"
