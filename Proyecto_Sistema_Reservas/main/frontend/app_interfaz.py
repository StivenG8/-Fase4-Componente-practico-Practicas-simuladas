import tkinter as tk
from tkinter import messagebox
import logging

from main.entidades.cliente import Cliente
from main.entidades.reserva import Reserva
from main.servicios.sala import ServicioSala
from main.servicios.equipo import ServicioEquipo
from main.servicios.asesoria import ServicioAsesoria
from main.excepciones.errores import ErrorValidacion, ErrorReserva

class InterfazSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestión de Reservas")
        self.root.geometry("600x500")
        
        # Datos en memoria (Backend)
        self.cliente_actual = None # El usuario logueado/registrado
        self.clientes = []
        self.servicios = [
            ServicioSala("S01", "Sala de Juntas", 50000),
            ServicioEquipo("E01", "Proyector 4K", 80000),
            ServicioAsesoria("A01", "Asesoría IT", 120000)
        ]
        self.reservas = []
        
        # Contenedor principal
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        
        # Diccionario de pantallas
        self.frames = {}
        
        # Inicializar todas las pantallas
        for F in (PantallaRegistro, PantallaMenu, PantallaReservas, PantallaHistorial):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Se apilan una encima de otra; la que se llame con tkraise() quedará visible
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Iniciar en la pantalla de registro
        self.mostrar_pantalla("PantallaRegistro")

    def mostrar_pantalla(self, page_name):
        """Muestra una pantalla por su nombre."""
        frame = self.frames[page_name]
        # Actualizar datos si la pantalla tiene un método de actualización
        if hasattr(frame, "actualizar_vista"):
            frame.actualizar_vista()
        frame.tkraise()


class PantallaRegistro(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="Registro de Usuario", font=("Arial", 18, "bold")).pack(pady=20)
        
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="ID de Cliente:").grid(row=0, column=0, pady=5, sticky="e")
        self.ent_id = tk.Entry(form_frame)
        self.ent_id.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Nombre Completo:").grid(row=1, column=0, pady=5, sticky="e")
        self.ent_nombre = tk.Entry(form_frame)
        self.ent_nombre.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(form_frame, text="Correo Electrónico:").grid(row=2, column=0, pady=5, sticky="e")
        self.ent_correo = tk.Entry(form_frame)
        self.ent_correo.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Button(self, text="Registrarse e Ingresar", command=self.registrar, bg="lightgreen", font=("Arial", 12)).pack(pady=20)
        
    def registrar(self):
        try:
            cid = self.ent_id.get().strip()
            nombre = self.ent_nombre.get().strip()
            correo = self.ent_correo.get().strip()
            
            # Crear y validar a través del backend
            cliente = Cliente(cid, nombre, correo)
            
            self.controller.clientes.append(cliente)
            self.controller.cliente_actual = cliente
            
            # Limpiar campos
            self.ent_id.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
            self.ent_correo.delete(0, tk.END)
            
            messagebox.showinfo("Bienvenido", f"¡Hola, {nombre}! Registro exitoso.")
            self.controller.mostrar_pantalla("PantallaMenu")
            
        except ErrorValidacion as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))


class PantallaMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.lbl_bienvenida = tk.Label(self, text="Menú Principal", font=("Arial", 18, "bold"))
        self.lbl_bienvenida.pack(pady=20)
        
        btn_reservas = tk.Button(self, text="📅 Nueva Reserva", font=("Arial", 12), width=25, command=lambda: controller.mostrar_pantalla("PantallaReservas"))
        btn_reservas.pack(pady=10)
        
        btn_historial = tk.Button(self, text="📊 Ver Historial de Reservas", font=("Arial", 12), width=25, command=lambda: controller.mostrar_pantalla("PantallaHistorial"))
        btn_historial.pack(pady=10)
        
        btn_simulacion = tk.Button(self, text="🤖 Ejecutar Simulación 10 Pasos", font=("Arial", 12), width=25, bg="lightblue", command=self.ejecutar_simulacion)
        btn_simulacion.pack(pady=10)
        
        btn_salir = tk.Button(self, text="Cerrar Sesión", font=("Arial", 10), width=20, fg="red", command=lambda: controller.mostrar_pantalla("PantallaRegistro"))
        btn_salir.pack(side="bottom", pady=20)

    def actualizar_vista(self):
        if self.controller.cliente_actual:
            self.lbl_bienvenida.config(text=f"Bienvenido, {self.controller.cliente_actual.get_nombre()}")

    def ejecutar_simulacion(self):
        """Ejecuta una simulación completa (10 escenarios)"""
        logging.info("--- NUEVA EJECUCIÓN DE SIMULACIÓN AUTOMATIZADA ---")
        
        try:
            # 1. Valido
            c1 = Cliente(123456, "Juan Perez", "juan@correo.com")
            self.controller.clientes.append(c1)
        except: pass
        
        # 2, 3. Inválidos (Se capturan y no crashea)
        try: Cliente(1, "", "juan")
        except: pass
        try: Cliente(123456, "Ana", "anacorreo.com")
        except: pass
        
        # Reservas
        if self.controller.clientes:
            # 5 y 6. Validas
            r1 = Reserva("SIM1", self.controller.clientes[-1], self.controller.servicios[0], 4)
            r1.procesar_reserva()
            self.controller.reservas.append(r1)
            
            r2 = Reserva("SIM2", self.controller.clientes[-1], self.controller.servicios[1], 2)
            r2.procesar_reserva(descuento=0.1, impuesto=0.19)
            self.controller.reservas.append(r2)
            
            # 7 y 8. Fallidas
            r3 = Reserva("SIM3", self.controller.clientes[-1], self.controller.servicios[2], -2)
            try: r3.procesar_reserva()
            except: pass
            self.controller.reservas.append(r3)
            
            r4 = Reserva("SIM4", self.controller.clientes[-1], self.controller.servicios[0], 1)
            r4.cancelar()
            try: r4.procesar_reserva()
            except: pass
            self.controller.reservas.append(r4)
            
            # 9. Datos corruptos
            try:
                c_malo = Cliente.__new__(Cliente)
                s_malo = ServicioSala.__new__(ServicioSala)
                s_malo._costo_base = 50000
                r5 = Reserva("SIM5", c_malo, s_malo, 2)
                r5.procesar_reserva(descuento=2.0)
            except ErrorReserva:
                pass
                
            # 10. Prueba de estabilidad final
            c_final = Cliente(889977, "Maria", "maria@correo.com")
            self.controller.clientes.append(c_final)
            r6 = Reserva("SIM6", c_final, self.controller.servicios[2], 5)
            r6.procesar_reserva()
            self.controller.reservas.append(r6)
            
        messagebox.showinfo("Simulación Completa", "Se ejecutaron los 10 escenarios.\nTodos los errores fueron capturados sin cerrar la app.\n\nRevisa el archivo errores_sistema.log para ver el detalle.")


class PantallaReservas(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="Crear Nueva Reserva", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.lbl_cliente_activo = tk.Label(self, text="Cliente: ", fg="blue", font=("Arial", 11))
        self.lbl_cliente_activo.pack(pady=5)
        
        frame_form = tk.Frame(self)
        frame_form.pack(pady=10)
        
        tk.Label(frame_form, text="Seleccione un Servicio:").grid(row=0, column=0, columnspan=2)
        
        self.box_servicio = tk.Listbox(frame_form, height=4, exportselection=False)
        self.box_servicio.grid(row=1, column=0, columnspan=2, pady=5)
        self.box_servicio.bind('<<ListboxSelect>>', self.mostrar_desc_servicio)
        
        self.lbl_desc_servicio = tk.Label(frame_form, text="[Seleccione un servicio]", fg="gray")
        self.lbl_desc_servicio.grid(row=2, column=0, columnspan=2, pady=5)
        
        tk.Label(frame_form, text="Tiempo (horas):").grid(row=3, column=0, sticky="e", pady=10)
        self.ent_tiempo = tk.Entry(frame_form, width=10)
        self.ent_tiempo.grid(row=3, column=1, sticky="w", padx=5)
        
        tk.Button(self, text="Confirmar Reserva", bg="lightgreen", command=self.crear_reserva).pack(pady=10)
        
        tk.Button(self, text="Volver al Menú", command=lambda: controller.mostrar_pantalla("PantallaMenu")).pack(pady=20)

    def actualizar_vista(self):
        if self.controller.cliente_actual:
            self.lbl_cliente_activo.config(text=f"Reserva a nombre de: {self.controller.cliente_actual.get_nombre()}")
            
        self.box_servicio.delete(0, tk.END)
        for s in self.controller.servicios:
            self.box_servicio.insert(tk.END, s.get_nombre())

    def mostrar_desc_servicio(self, event):
        sel = self.box_servicio.curselection()
        if sel:
            servicio = self.controller.servicios[sel[0]]
            desc = f"{servicio.get_nombre()} | Costo base/hr: ${servicio._costo_base}"
            self.lbl_desc_servicio.config(text=desc)

    def crear_reserva(self):
        try:
            sel_ser = self.box_servicio.curselection()
            if not sel_ser:
                raise ErrorValidacion("Debe seleccionar un servicio.")
                
            cliente = self.controller.cliente_actual
            servicio = self.controller.servicios[sel_ser[0]]
            
            tiempo_str = self.ent_tiempo.get()
            if not tiempo_str.isdigit():
                raise ErrorValidacion("El tiempo debe ser un número entero.")
                
            tiempo = int(tiempo_str)
            
            reserva = Reserva(f"R{len(self.controller.reservas)+1:03d}", cliente, servicio, tiempo)
            reserva.procesar_reserva(descuento=0.0, impuesto=0.19)
            
            self.controller.reservas.append(reserva)
            
            if reserva.estado == "Confirmada":
                messagebox.showinfo("Reserva Confirmada", f"Reserva exitosa.\nTotal a pagar: ${reserva.costo_total:.2f}")
                self.ent_tiempo.delete(0, tk.END)
            else:
                messagebox.showwarning("Reserva Fallida", "La reserva no pudo procesarse. Revise los logs.")
                
        except (ErrorValidacion, ErrorReserva) as e:
            messagebox.showerror("Error del Sistema", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))


class PantallaHistorial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tk.Label(self, text="Historial de Reservas Global", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.lst_reservas = tk.Listbox(self, width=60, height=15)
        self.lst_reservas.pack(pady=10, padx=20)
        
        tk.Button(self, text="Actualizar Lista", command=self.actualizar_vista).pack(pady=5)
        tk.Button(self, text="Volver al Menú", command=lambda: controller.mostrar_pantalla("PantallaMenu")).pack(pady=10)

    def actualizar_vista(self):
        self.lst_reservas.delete(0, tk.END)
        if not self.controller.reservas:
            self.lst_reservas.insert(tk.END, "Aún no hay reservas en el sistema.")
        else:
            for r in self.controller.reservas:
                self.lst_reservas.insert(tk.END, str(r))
