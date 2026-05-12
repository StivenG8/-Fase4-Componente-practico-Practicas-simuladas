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
        
        self.clientes = []
        self.servicios = [
            ServicioSala("S01", "Sala de Juntas", 50000),
            ServicioEquipo("E01", "Proyector 4K", 80000),
            ServicioAsesoria("A01", "Asesoría IT", 120000)
        ]
        self.reservas = []
        
        # Interfaz de Cliente
        frame_cliente = tk.LabelFrame(self.root, text="Gestión de Clientes")
        frame_cliente.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame_cliente, text="ID:").grid(row=0, column=0)
        self.ent_id = tk.Entry(frame_cliente)
        self.ent_id.grid(row=0, column=1)
        
        tk.Label(frame_cliente, text="Nombre:").grid(row=1, column=0)
        self.ent_nombre = tk.Entry(frame_cliente)
        self.ent_nombre.grid(row=1, column=1)
        
        tk.Label(frame_cliente, text="Correo:").grid(row=2, column=0)
        self.ent_correo = tk.Entry(frame_cliente)
        self.ent_correo.grid(row=2, column=1)
        
        tk.Button(frame_cliente, text="Crear Cliente", command=self.crear_cliente).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Interfaz de Reserva
        frame_reserva = tk.LabelFrame(self.root, text="Gestión de Reservas")
        frame_reserva.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame_reserva, text="Cliente:").grid(row=0, column=0)
        self.box_cliente = tk.Listbox(frame_reserva, height=3, exportselection=False)
        self.box_cliente.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_reserva, text="Servicio:").grid(row=0, column=2)
        self.box_servicio = tk.Listbox(frame_reserva, height=3, exportselection=False)
        self.box_servicio.grid(row=0, column=3, padx=5)
        self.box_servicio.bind('<<ListboxSelect>>', self.mostrar_desc_servicio)
        
        tk.Label(frame_reserva, text="Tiempo (horas):").grid(row=1, column=0)
        self.ent_tiempo = tk.Entry(frame_reserva)
        self.ent_tiempo.grid(row=1, column=1)
        
        self.lbl_desc_servicio = tk.Label(frame_reserva, text="[Seleccione un servicio]", fg="gray", wraplength=150)
        self.lbl_desc_servicio.grid(row=1, column=2, columnspan=2)
        
        tk.Button(frame_reserva, text="Procesar Reserva", command=self.crear_reserva).grid(row=2, column=0, columnspan=4, pady=5)
        
        # Lista de Reservas (Log)
        frame_logs = tk.LabelFrame(self.root, text="Reservas Registradas")
        frame_logs.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.lst_reservas = tk.Listbox(frame_logs)
        self.lst_reservas.pack(fill=tk.BOTH, expand=True)

        # Botón de Simulación Automatizada
        tk.Button(self.root, text="Ejecutar Simulación 10 Escenarios", command=self.ejecutar_simulacion, bg="lightblue").pack(fill=tk.X, padx=10, pady=10)

        self.actualizar_listas()

    def actualizar_listas(self):
        self.box_cliente.delete(0, tk.END)
        for c in self.clientes:
            self.box_cliente.insert(tk.END, c.get_nombre())
            
        self.box_servicio.delete(0, tk.END)
        for s in self.servicios:
            self.box_servicio.insert(tk.END, s.get_nombre())
            
        self.lst_reservas.delete(0, tk.END)
        for r in self.reservas:
            self.lst_reservas.insert(tk.END, str(r))

    def mostrar_desc_servicio(self, event):
        sel = self.box_servicio.curselection()
        if sel:
            servicio = self.servicios[sel[0]]
            desc = f"{servicio.get_nombre()} | Costo/hr: ${servicio._costo_base}"
            self.lbl_desc_servicio.config(text=desc)

    def crear_cliente(self):
        try:
            cid = self.ent_id.get().strip()
            nombre = self.ent_nombre.get().strip()
            correo = self.ent_correo.get().strip()
            
            cliente = Cliente(cid, nombre, correo)
            self.clientes.append(cliente)
            self.actualizar_listas()
            
            # Limpiar los campos
            self.ent_id.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
            self.ent_correo.delete(0, tk.END)
            
            messagebox.showinfo("Éxito", f"Cliente {nombre} creado correctamente.")
            
        except ErrorValidacion as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error Desconocido", str(e))

    def crear_reserva(self):
        try:
            sel_cli = self.box_cliente.curselection()
            sel_ser = self.box_servicio.curselection()
            
            if not sel_cli or not sel_ser:
                raise ErrorValidacion("Debe seleccionar un cliente y un servicio.")
                
            cliente = self.clientes[sel_cli[0]]
            servicio = self.servicios[sel_ser[0]]
            
            tiempo_str = self.ent_tiempo.get()
            if not tiempo_str.isdigit():
                raise ErrorValidacion("El tiempo debe ser un número entero.")
                
            tiempo = int(tiempo_str)
            
            reserva = Reserva(f"R{len(self.reservas)+1:03d}", cliente, servicio, tiempo)
            # Demostramos sobrecarga aquí pasando parámetros opcionales
            reserva.procesar_reserva(descuento=0.05, impuesto=0.19)
            
            self.reservas.append(reserva)
            self.actualizar_listas()
            
            if reserva.estado == "Confirmada":
                messagebox.showinfo("Reserva Confirmada", f"Total: ${reserva.costo_total:.2f}")
            else:
                messagebox.showwarning("Reserva Fallida", "La reserva no pudo procesarse. Revise los logs.")
                
        except (ErrorValidacion, ErrorReserva) as e:
            messagebox.showerror("Error del Sistema", str(e))
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))

    def ejecutar_simulacion(self):
        """Ejecuta una simulación completa (10 escenarios) y lo refleja en la interfaz"""
        from main.entidades.cliente import Cliente
        from main.entidades.reserva import Reserva
        
        logging.info("--- NUEVA EJECUCIÓN DE SIMULACIÓN AUTOMATIZADA ---")
        
        try:
            # 1. Valido
            c1 = Cliente(123456, "Juan Perez", "juan@correo.com")
            self.clientes.append(c1)
        except: pass
        
        # 2, 3. Inválidos (Se capturan y no crashea)
        try: Cliente(1, "", "juan")
        except: pass
        try: Cliente(123456, "Ana", "anacorreo.com")
        except: pass
        
        # Reservas
        if self.clientes:
            # 5 y 6. Validas
            r1 = Reserva("SIM1", self.clientes[0], self.servicios[0], 4)
            r1.procesar_reserva()
            self.reservas.append(r1)
            
            r2 = Reserva("SIM2", self.clientes[0], self.servicios[1], 2)
            r2.procesar_reserva(descuento=0.1, impuesto=0.19)
            self.reservas.append(r2)
            
            # 7 y 8. Fallidas
            r3 = Reserva("SIM3", self.clientes[0], self.servicios[2], -2)
            try: r3.procesar_reserva()
            except: pass
            self.reservas.append(r3)
            
            r4 = Reserva("SIM4", self.clientes[0], self.servicios[0], 1)
            r4.cancelar()
            try: r4.procesar_reserva()
            except: pass
            self.reservas.append(r4)
            
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
            self.clientes.append(c_final)
            r6 = Reserva("SIM6", c_final, self.servicios[2], 5)
            r6.procesar_reserva()
            self.reservas.append(r6)
            
        self.actualizar_listas()
        messagebox.showinfo("Simulación Completa", "Se ejecutaron los 10 escenarios. Revisa el archivo errores_sistema.log para ver las excepciones capturadas y encadenadas.")
