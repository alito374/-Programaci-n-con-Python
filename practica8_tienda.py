import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class PuntoDeVentaZapateria:
    def __init__(self, root):
        self.root = root
        self.root.title("Zapatería - Sistema de Ventas")
        self.root.geometry("1024x720")
        self.root.configure(bg="#F4EAEF")
        self.root.resizable(False, False)

        # Configuración de Estilos (Inspirado en la interfaz de Pinky Paper)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Paleta de colores: Rosa pastel, amarillo suave, blanco y acentos oscuros
        self.COLOR_BG = "#F4EAEF"
        self.COLOR_SIDEBAR = "#FAF0B2"
        self.COLOR_HEADER = "#E8B4CB"
        self.COLOR_ACCENT = "#D17A9B"
        self.COLOR_WHITE = "#FFFFFF"
        self.COLOR_TEXT = "#333333"

        # Datos en memoria (Simulación de BD)
        self.productos = {
            "Z01": {"nombre": "Tenis Casual Blanco", "precio": 850.00, "existencias": 12},
            "Z02": {"nombre": "Botín de Piel Negro", "precio": 1200.00, "existencias": 8},
            "Z03": {"nombre": "Zapato Formal Oxford", "precio": 990.00, "existencias": 10}
        }
        self.clientes = {
            "7731234567": {"nombre": "Mónica", "correo": "monigail@mail.com"}
        }
        self.ventas_carrito = []
        self.historial_tickets = []

        # Construir Interfaz Principal
        self.crear_header()
        self.crear_sidebar()
        self.crear_contenedor_principal()
        
        # Mostrar vista inicial (Productos)
        self.mostrar_productos()

    def crear_header(self):
        header_frame = tk.Frame(self.root, bg=self.COLOR_HEADER, height=80)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)

        titulo = tk.Label(header_frame, text="Zapatería Elegance", font=("Arial", 22, "bold"), bg=self.COLOR_HEADER, fg="#4A2E3B")
        titulo.pack(pady=10)
        subtitulo = tk.Label(header_frame, text="Calzado, estilo y confort", font=("Arial", 10, "italic"), bg=self.COLOR_HEADER, fg="#5C3D4C")
        subtitulo.pack()

    def crear_sidebar(self):
        self.sidebar_frame = tk.Frame(self.root, bg=self.COLOR_SIDEBAR, width=220, height=640)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)

        botones = [
            ("Inicio", self.mostrar_inicio),
            ("Productos", self.mostrar_productos),
            ("Clientes", self.mostrar_clientes),
            ("Ventas", self.mostrar_ventas),
            ("Tickets", self.mostrar_tickets),
            ("Config / Regenerar", self.mostrar_regenerador)
        ]

        tk.Label(self.sidebar_frame, text="Menú", font=("Arial", 12, "bold"), bg=self.COLOR_SIDEBAR, fg="#5C3D4C").pack(pady=20)

        for texto, comando in botones:
            btn = tk.Button(self.sidebar_frame, text=texto, font=("Arial", 11), bg=self.COLOR_SIDEBAR, fg=self.COLOR_TEXT,
                            bd=0, activebackground=self.COLOR_HEADER, activeforeground="black", anchor="w", padx=25, command=comando)
            btn.pack(fill=tk.X, pady=4)

        btn_salir = tk.Button(self.sidebar_frame, text="Cerrar sesión", font=("Arial", 10, "bold"), bg=self.COLOR_HEADER, fg="#4A2E3B",
                              bd=0, command=self.root.quit, padx=25, pady=8)
        btn_salir.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=20)

    def crear_contenedor_principal(self):
        self.main_container = tk.Frame(self.root, bg=self.COLOR_BG)
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def limpiar_contenedor(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # ==================== VISTA: INICIO ====================
    def mostrar_inicio(self):
        self.limpiar_contenedor()
        tk.Label(self.main_container, text="Bienvenido al Sistema de Punto de Venta", font=("Arial", 18, "bold"), bg=self.COLOR_BG, fg=self.COLOR_TEXT).pack(pady=40)
        tk.Label(self.main_container, text="Selecciona una opción del menú lateral para comenzar a administrar tu zapatería.", font=("Arial", 12), bg=self.COLOR_BG, fg="#666").pack(pady=10)

    # ==================== VISTA: PRODUCTOS ====================
    def mostrar_productos(self):
        self.limpiar_contenedor()
        
        tk.Label(self.main_container, text="Administración de Productos", font=("Arial", 18, "bold"), bg=self.COLOR_BG, fg=self.COLOR_TEXT).place(x=40, y=30)

        # Formulario
        tk.Label(self.main_container, text="Código:", font=("Arial", 10), bg=self.COLOR_BG).place(x=40, y=90)
        self.entry_p_codigo = tk.Entry(self.main_container, font=("Arial", 11), width=15)
        self.entry_p_codigo.place(x=100, y=90)

        tk.Label(self.main_container, text="Nombre:", font=("Arial", 10), bg=self.COLOR_BG).place(x=240, y=90)
        self.entry_p_nombre = tk.Entry(self.main_container, font=("Arial", 11), width=25)
        self.entry_p_nombre.place(x=300, y=90)

        tk.Label(self.main_container, text="Precio:", font=("Arial", 10), bg=self.COLOR_BG).place(x=40, y=135)
        self.entry_p_precio = tk.Entry(self.main_container, font=("Arial", 11), width=15)
        self.entry_p_precio.place(x=100, y=135)

        tk.Label(self.main_container, text="Existencias:", font=("Arial", 10), bg=self.COLOR_BG).place(x=220, y=135)
        self.entry_p_existencias = tk.Entry(self.main_container, font=("Arial", 11), width=15)
        self.entry_p_existencias.place(x=300, y=135)

        btn_registrar = tk.Button(self.main_container, text="Registrar producto", font=("Arial", 10, "bold"), bg=self.COLOR_HEADER, fg="#4A2E3B", bd=0, padx=10, pady=5, command=self.registrar_producto)
        btn_registrar.place(x=40, y=185)

        # Tabla de productos
        self.tabla_productos = ttk.Treeview(self.main_container, columns=("Codigo", "Producto", "Precio", "Existencias"), show="headings", height=14)
        self.tabla_productos.heading("Codigo", text="Código")
        self.tabla_productos.heading("Producto", text="Producto")
        self.tabla_productos.heading("Precio", text="Precio")
        self.tabla_productos.heading("Existencias", text="Existencias")
        
        self.tabla_productos.column("Codigo", width=100, anchor="center")
        self.tabla_productos.column("Producto", width=250, anchor="w")
        self.tabla_productos.column("Precio", width=120, anchor="center")
        self.tabla_productos.column("Existencias", width=120, anchor="center")
        
        self.tabla_productos.place(x=40, y=240, width=590, height=360)

        self.actualizar_tabla_productos()

    def registrar_producto(self):
        c = self.entry_p_codigo.get().strip()
        n = self.entry_p_nombre.get().strip()
        p = self.entry_p_precio.get().strip()
        e = self.entry_p_existencias.get().strip()

        if not c or not n or not p or not e:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        try:
            precio_f = float(p)
            exist_i = int(e)
        except ValueError:
            messagebox.showerror("Error", "Precio y existencias deben ser numéricos.")
            return

        self.productos[c] = {"nombre": n, "precio": precio_f, "existencias": exist_i}
        messagebox.showinfo("Éxito", "Producto registrado correctamente.")
        self.actualizar_tabla_productos()
        self.entry_p_codigo.delete(0, tk.END)
        self.entry_p_nombre.delete(0, tk.END)
        self.entry_p_precio.delete(0, tk.END)
        self.entry_p_existencias.delete(0, tk.END)

    def actualizar_tabla_productos(self):
        for row in self.tabla_productos.get_children():
            self.tabla_productos.delete(row)
        for c, datos in self.productos.items():
            self.tabla_productos.insert("", tk.END, values=(c, datos["nombre"], f"${datos['precio']:.2f}", datos["existencias"]))

    # ==================== VISTA: CLIENTES ====================
    def mostrar_clientes(self):
        self.limpiar_contenedor()
        tk.Label(self.main_container, text="Registro de Clientes", font=("Arial", 18, "bold"), bg=self.COLOR_BG, fg=self.COLOR_TEXT).place(x=40, y=30)

        tk.Label(self.main_container, text="Nombre:", font=("Arial", 10), bg=self.COLOR_BG).place(x=40, y=90)
        self.entry_c_nombre = tk.Entry(self.main_container, font=("Arial", 11), width=20)
        self.entry_c_nombre.place(x=100, y=90)

        tk.Label(self.main_container, text="Teléfono:", font=("Arial", 10), bg=self.COLOR_BG).place(x=300, y=90)
        self.entry_c_telefono = tk.Entry(self.main_container, font=("Arial", 11), width=18)
        self.entry_c_telefono.place(x=370, y=90)

        tk.Label(self.main_container, text="Correo:", font=("Arial", 10), bg=self.COLOR_BG).place(x=40, y=135)
        self.entry_c_correo = tk.Entry(self.main_container, font=("Arial", 11), width=30)
        self.entry_c_correo.place(x=100, y=135)

        btn_reg_cliente = tk.Button(self.main_container, text="Registrar cliente", font=("Arial", 10, "bold"), bg=self.COLOR_HEADER, fg="#4A2E3B", bd=0, padx=10, pady=5, command=self.registrar_cliente)
        btn_reg_cliente.place(x=40, y=185)

        self.tabla_clientes = ttk.Treeview(self.main_container, columns=("Nombre", "Telefono", "Correo"), show="headings", height=14)
        self.tabla_clientes.heading("Nombre", text="Nombre")
        self.tabla_clientes.heading("Telefono", text="Teléfono")
        self.tabla_clientes.heading("Correo", text="Correo electrónico")

        self.tabla_clientes.column("Nombre", width=180, anchor="w")
        self.tabla_clientes.column("Telefono", width=150, anchor="center")
        self.tabla_clientes.column("Correo", width=260, anchor="w")

        self.tabla_clientes.place(x=40, y=240, width=590, height=360)
        self.actualizar_tabla_clientes()

    def registrar_cliente(self):
        n = self.entry_c_nombre.get().strip()
        t = self.entry_c_telefono.get().strip()
        c = self.entry_c_correo.get().strip()

        if not n or not t:
            messagebox.showerror("Error", "Nombre y teléfono son obligatorios.")
            return

        self.clientes[t] = {"nombre": n, "correo": c}
        messagebox.showinfo("Éxito", "Cliente registrado exitosamente.")
        self.actualizar_tabla_clientes()
        self.entry_c_nombre.delete(0, tk.END)
        self.entry_c_telefono.delete(0, tk.END)
        self.entry_c_correo.delete(0, tk.END)

    def actualizar_tabla_clientes(self):
        for row in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(row)
        for t, datos in self.clientes.items():
            self.tabla_clientes.insert("", tk.END, values=(datos["nombre"], t, datos["correo"]))

    # ==================== VISTA: VENTAS ====================
    def mostrar_ventas(self):
        self.limpiar_contenedor()
        tk.Label(self.main_container, text="Registro de Ventas", font=("Arial", 18, "bold"), bg=self.COLOR_BG, fg=self.COLOR_TEXT).place(x=40, y=30)

        tk.Label(self.main_container, text="Cliente:", font=("Arial", 10), bg=self.COLOR_BG).place(x=40, y=85)
        self.combo_cliente = ttk.Combobox(self.main_container, values=[f"{d['nombre']} ({t})" for t, d in self.clientes.items()], width=35, state="readonly")
        self.combo_cliente.place(x=140, y=85)
        if self.clientes:
            self.combo_cliente.current(0)

        tk.Label(self.main_container, text="Código de producto:", font=("Arial", 10), bg=self.COLOR_BG).place(x=40, y=125)
        self.combo_prod = ttk.Combobox(self.main_container, values=[f"{c} - {d['nombre']} (${d['precio']})" for c, d in self.productos.items()], width=35, state="readonly")
        self.combo_prod.place(x=140, y=125)
        if self.productos:
            self.combo_prod.current(0)

        tk.Label(self.main_container, text="Cantidad:", font=("Arial", 10), bg=self.COLOR_BG).place(x=40, y=165)
        self.entry_v_cant = tk.Entry(self.main_container, font=("Arial", 11), width=10)
        self.entry_v_cant.insert(0, "1")
        self.entry_v_cant.place(x=140, y=165)

        btn_add = tk.Button(self.main_container, text="Agregar producto", font=("Arial", 10, "bold"), bg=self.COLOR_HEADER, fg="#4A2E3B", bd=0, padx=10, pady=4, command=self.agregar_a_carrito)
        btn_add.place(x=250, y=162)

        # Tabla del carrito
        self.tabla_carrito = ttk.Treeview(self.main_container, columns=("Codigo", "Producto", "Cantidad", "Precio", "Importe"), show="headings", height=10)
        self.tabla_carrito.heading("Codigo", text="Código")
        self.tabla_carrito.heading("Producto", text="Producto")
        self.tabla_carrito.heading("Cantidad", text="Cantidad")
        self.tabla_carrito.heading("Precio", text="Precio unitario")
        self.tabla_carrito.heading("Importe", text="Importe")

        self.tabla_carrito.column("Codigo", width=80, anchor="center")
        self.tabla_carrito.column("Producto", width=220, anchor="w")
        self.tabla_carrito.column("Cantidad", width=80, anchor="center")
        self.tabla_carrito.column("Precio", width=100, anchor="center")
        self.tabla_carrito.column("Importe", width=100, anchor="center")

        self.tabla_carrito.place(x=40, y=210, width=580, height=240)

        # Totales
        self.lbl_subtotal = tk.Label(self.main_container, text="Subtotal: $0.00", font=("Arial", 11, "bold"), bg=self.COLOR_SIDEBAR, fg=self.COLOR_TEXT, padx=15, pady=5)
        self.lbl_subtotal.place(x=340, y=470)

        self.lbl_total = tk.Label(self.main_container, text="Total: $0.00", font=("Arial", 11, "bold"), bg=self.COLOR_SIDEBAR, fg=self.COLOR_TEXT, padx=15, pady=5)
        self.lbl_total.place(x=490, y=470)

        btn_finalizar = tk.Button(self.main_container, text="Finalizar venta y generar ticket", font=("Arial", 11, "bold"), bg=self.COLOR_ACCENT, fg="white", bd=0, padx=15, pady=8, command=self.finalizar_venta)
        btn_finalizar.place(x=360, y=530)

        self.ventas_carrito = []

    def agregar_a_carrito(self):
        sel_prod = self.combo_prod.get()
        if not sel_prod:
            return
        codigo = sel_prod.split(" - ")[0]
        try:
            cant = int(self.entry_v_cant.get())
            if cant <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return

        prod = self.productos[codigo]
        if prod["existencias"] < cant:
            messagebox.showerror("Stock insuficiente", f"Solo quedan {prod['existencias']} unidades en stock.")
            return

        importe = prod["precio"] * cant
        self.ventas_carrito.append({"codigo": codigo, "nombre": prod["nombre"], "cantidad": cant, "precio": prod["precio"], "importe": importe})
        
        # Descontar stock temporalmente
        prod["existencias"] -= cant

        self.actualizar_tabla_carrito()

    def actualizar_tabla_carrito(self):
        for row in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(row)
        
        subtotal = 0
        for item in self.ventas_carrito:
            self.tabla_carrito.insert("", tk.END, values=(item["codigo"], item["nombre"], item["cantidad"], f"${item['precio']:.2f}", f"${item['importe']:.2f}"))
            subtotal += item["importe"]

        self.lbl_subtotal.config(text=f"Subtotal: ${subtotal:.2f}")
        self.lbl_total.config(text=f"Total: ${subtotal:.2f}")

    def finalizar_venta(self):
        if not self.ventas_carrito:
            messagebox.showwarning("Aviso", "El carrito de ventas está vacío.")
            return

        cliente = self.combo_cliente.get()
        cliente_nombre = cliente.split(" (")[0] if cliente else "General"
        subtotal = sum(i["importe"] for i in self.ventas_carrito)
        
        folio = len(self.historial_tickets) + 1
        fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        
        ticket = {
            "folio": folio,
            "fecha": fecha,
            "cliente": cliente_nombre,
            "productos": list(self.ventas_carrito),
            "total": subtotal
        }
        self.historial_tickets.append(ticket)
        messagebox.showinfo("Ticket Generado", f"Venta registrada con éxito.\nFolio #{folio}\nTotal: ${subtotal:.2f}")
        
        self.ventas_carrito = []
        self.mostrar_ventas()

    # ==================== VISTA: TICKETS ====================
    def mostrar_tickets(self):
        self.limpiar_contenedor()
        tk.Label(self.main_container, text="Historial de Tickets", font=("Arial", 18, "bold"), bg=self.COLOR_BG, fg=self.COLOR_TEXT).place(x=40, y=30)

        self.tabla_tickets = ttk.Treeview(self.main_container, columns=("Folio", "Fecha", "Cliente", "Total"), show="headings", height=15)
        self.tabla_tickets.heading("Folio", text="Folio")
        self.tabla_tickets.heading("Fecha", text="Fecha")
        self.tabla_tickets.heading("Cliente", text="Cliente")
        self.tabla_tickets.heading("Total", text="Total")

        self.tabla_tickets.column("Folio", width=80, anchor="center")
        self.tabla_tickets.column("Fecha", width=160, anchor="center")
        self.tabla_tickets.column("Cliente", width=200, anchor="w")
        self.tabla_tickets.column("Total", width=120, anchor="center")

        self.tabla_tickets.place(x=40, y=90, width=580, height=380)

        for t in self.historial_tickets:
            self.tabla_tickets.insert("", tk.END, values=(t["folio"], t["fecha"], t["cliente"], f"${t['total']:.2f}"))

        btn_ver = tk.Button(self.main_container, text="Ver ticket seleccionado", font=("Arial", 10, "bold"), bg=self.COLOR_HEADER, fg="#4A2E3B", bd=0, padx=12, pady=6, command=self.ver_detalle_ticket)
        btn_ver.place(x=240, y=490)

    def ver_detalle_ticket(self):
        sel = self.tabla_tickets.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un ticket del historial.")
            return
        item_vals = self.tabla_tickets.item(sel[0], "values")
        folio = int(item_vals[0])
        
        ticket = next((t for t in self.historial_tickets if t["folio"] == folio), None)
        if ticket:
            detalle = f"TICKET DE VENTA #{ticket['folio']}\nFecha: {ticket['fecha']}\nCliente: {ticket['cliente']}\n----------------------------------\n"
            for p in ticket["productos"]:
                detalle += f"{p['cantidad']}x {p['nombre']} - ${p['importe']:.2f}\n"
            detalle += f"----------------------------------\nTOTAL: ${ticket['total']:.2f}"
            messagebox.showinfo(f"Ticket #{folio}", detalle)

    # ==================== REGENERAR / CONFIGURAR NUEVO PRODUCTO ====================
    def mostrar_regenerador(self):
        self.limpiar_contenedor()
        tk.Label(self.main_container, text="Regenerar / Configurar Nuevo Ramo", font=("Arial", 18, "bold"), bg=self.COLOR_BG, fg=self.COLOR_TEXT).place(x=40, y=30)
        
        tk.Label(self.main_container, text="Puedes reconfigurar este punto de venta para vender cualquier otro tipo\nde producto (ej. Ropa, Electrónica, Papelería, Accesorios, etc.):", font=("Arial", 11), bg=self.COLOR_BG, fg="#555", justify="left").place(x=40, y=85)

        tk.Label(self.main_container, text="Nombre del Negocio / Tienda:", font=("Arial", 10, "bold"), bg=self.COLOR_BG).place(x=40, y=150)
        self.entry_nuevo_negocio = tk.Entry(self.main_container, font=("Arial", 11), width=30)
        self.entry_nuevo_negocio.insert(0, "Boutique Fashion")
        self.entry_nuevo_negocio.place(x=40, y=180)

        tk.Label(self.main_container, text="Ejemplo de producto inicial:", font=("Arial", 10, "bold"), bg=self.COLOR_BG).place(x=40, y=230)
        self.entry_nuevo_ejemplo = tk.Entry(self.main_container, font=("Arial", 11), width=30)
        self.entry_nuevo_ejemplo.insert(0, "Vestido de Seda")
        self.entry_nuevo_ejemplo.place(x=40, y=260)

        btn_regen = tk.Button(self.main_container, text="Regenerar Sistema POS", font=("Arial", 11, "bold"), bg=self.COLOR_ACCENT, fg="white", bd=0, padx=15, pady=10, command=self.ejecutar_regeneracion)
        btn_regen.place(x=40, y=320)

    def ejecutar_regeneracion(self):
        nuevo_nombre = self.entry_nuevo_negocio.get().strip()
        nuevo_prod = self.entry_nuevo_ejemplo.get().strip()
        if not nuevo_nombre or not nuevo_prod:
            messagebox.showerror("Error", "Completa los campos para regenerar.")
            return

        # Limpiar y redefinir inventario con el nuevo giro
        self.productos = {
            "P01": {"nombre": nuevo_prod, "precio": 450.00, "existencias": 15}
        }
        self.ventas_carrito = []
        self.historial_tickets = []
        
        messagebox.showinfo("¡Sistema Regenerado!", f"El punto de venta se ha reconfigurado para:\n'{nuevo_nombre}'\n¡Ya puedes registrar y vender {nuevo_prod}!")
        self.mostrar_productos()

if __name__ == "__main__":
    root = tk.Tk()
    app = PuntoDeVentaZapateria(root)
    root.mainloop()