from main.servicios.servicio_base import Servicio

class ServicioSala(Servicio):
    def calcular_costo(self, horas, descuento=0.0, impuesto=0.0):
        """Cálculo específico para alquiler de salas por hora."""
        subtotal = self._costo_base * horas
        total = subtotal - (subtotal * descuento) + (subtotal * impuesto)
        return total
