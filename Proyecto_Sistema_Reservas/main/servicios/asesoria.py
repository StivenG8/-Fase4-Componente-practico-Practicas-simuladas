from main.servicios.servicio_base import Servicio

class ServicioAsesoria(Servicio):
    def calcular_costo(self, sesiones, descuento=0.0, impuesto=0.0):
        """Cálculo específico para asesorías."""
        # Las asesorías tienen un descuento automático del 2% si son más de 3 sesiones
        if sesiones > 3:
            descuento += 0.02
        subtotal = self._costo_base * sesiones
        total = subtotal - (subtotal * descuento) + (subtotal * impuesto)
        return total
