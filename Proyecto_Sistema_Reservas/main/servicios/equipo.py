from main.servicios.servicio_base import Servicio

class ServicioEquipo(Servicio):
    def calcular_costo(self, dias, descuento=0.0, impuesto=0.0):
        """Cálculo específico para alquiler de equipos por día."""
        # Se aplica un recargo del 5% por mantenimiento
        recargo_mantenimiento = 0.05
        subtotal = (self._costo_base * dias) * (1 + recargo_mantenimiento)
        total = subtotal - (subtotal * descuento) + (subtotal * impuesto)
        return total
