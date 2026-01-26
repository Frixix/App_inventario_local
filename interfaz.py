"""
CAPA DE INTERFAZ - GUI con customtkinter
Aplicación de Escritorio para Inventario - Diseño Moderno
"""

import customtkinter as ctk
from tkinter import messagebox, scrolledtext
from datetime import datetime
from logica import LogicaInventario
from facturas import GeneradorFactura

# Configuración de tema
ctk.set_appearance_mode("light")

# Colores personalizados
FONDO = "#ECEFF1"
TARJETA = "#FFFFFF"
TEXTO = "#1F2933"
PRINCIPAL = "#0F766E"
SECUNDARIO = "#9CA3AF"
ERROR = "#DC2626"

class VentanaLogin(ctk.CTk):
    """Ventana de login moderna"""
    
    def __init__(self):
        super().__init__()
        self.title("Inventario - Login")
        self.geometry("420x380")
        self.resizable(False, False)
        self.configure(fg_color=FONDO)
        
        try:
            self.logica = LogicaInventario()
            self.crearUI()
        except Exception as e:
            messagebox.showerror("Error de Inicialización", 
                                f"Error al cargar la aplicación:\n{str(e)}")
            self.destroy()
    
    def crearUI(self):
        """Crea interfaz de login moderna"""
        # Frame principal centrado
        main_frame = ctk.CTkFrame(self, fg_color=FONDO)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Tarjeta de login
        card = ctk.CTkFrame(main_frame, fg_color=TARJETA, corner_radius=12)
        card.pack(fill=ctk.BOTH, expand=True, padx=0, pady=0)
        
        # Padding interno
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, expand=True, padx=30, pady=30)
        
        # Título
        titulo = ctk.CTkLabel(inner, text="Sistema de Inventario",
                             font=("Segoe UI", 24, "bold"),
                             text_color=TEXTO)
        titulo.pack(pady=(0, 10))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(inner, text="Ingrese sus credenciales",
                                font=("Segoe UI", 12),
                                text_color=SECUNDARIO)
        subtitulo.pack(pady=(0, 25))
        
        # Usuario
        ctk.CTkLabel(inner, text="Usuario:",
                    font=("Segoe UI", 11, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        
        self.entrada_usuario = ctk.CTkEntry(inner,
                                           placeholder_text="admin",
                                           height=40,
                                           border_width=1,
                                           border_color=SECUNDARIO,
                                           fg_color=TARJETA,
                                           text_color=TEXTO)
        self.entrada_usuario.pack(fill=ctk.X, pady=(0, 15))
        
        # Contraseña
        ctk.CTkLabel(inner, text="Contraseña:",
                    font=("Segoe UI", 11, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        
        self.entrada_contraseña = ctk.CTkEntry(inner,
                                              placeholder_text="1234",
                                              show="*",
                                              height=40,
                                              border_width=1,
                                              border_color=SECUNDARIO,
                                              fg_color=TARJETA,
                                              text_color=TEXTO)
        self.entrada_contraseña.pack(fill=ctk.X, pady=(0, 30))
        
        # Botón INGRESAR
        btn_login = ctk.CTkButton(inner,
                                 text="INGRESAR",
                                 command=self.hacer_login,
                                 fg_color=PRINCIPAL,
                                 hover_color="#0D5C5F",
                                 text_color="white",
                                 font=("Segoe UI", 13, "bold"),
                                 height=45,
                                 corner_radius=8)
        btn_login.pack(fill=ctk.X, pady=(0, 12))
        
        # Botón Salir
        btn_salir = ctk.CTkButton(inner,
                                 text="Salir",
                                 command=self.salir_app,
                                 fg_color=SECUNDARIO,
                                 hover_color="#8B92A8",
                                 text_color="white",
                                 font=("Segoe UI", 12),
                                 height=40,
                                 corner_radius=8)
        btn_salir.pack(fill=ctk.X)
        
        self.entrada_usuario.focus()
        
        # Permitir Enter
        self.entrada_usuario.bind("<Return>", lambda e: self.hacer_login())
        self.entrada_contraseña.bind("<Return>", lambda e: self.hacer_login())
    
    def hacer_login(self):
        """Valida credenciales"""
        try:
            usuario = self.entrada_usuario.get().strip()
            contraseña = self.entrada_contraseña.get()
            
            if not usuario or not contraseña:
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
            if self.logica.login(usuario, contraseña):
                self.destroy()
                try:
                    app = AplicacionInventario(self.logica)
                    app.mainloop()
                except Exception as e:
                    messagebox.showerror("Error", 
                        f"Error al abrir la aplicación:\n{str(e)}")
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                self.entrada_contraseña.delete(0, ctk.END)
                self.entrada_usuario.focus()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión:\n{str(e)}")
    
    def salir_app(self):
        """Cierra la aplicación correctamente"""
        if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
            self.destroy()


class AplicacionInventario(ctk.CTk):
    """Aplicación principal de inventario - Diseño Moderno"""
    
    def __init__(self, logica):
        super().__init__()
        self.title("Sistema de Inventario Local")
        self.geometry("1000x700")
        self.configure(fg_color=FONDO)
        self.logica = logica
        self.generador_facturas = GeneradorFactura(logica)
        self.factura_actual = None
        
        self.crearUI()
        self.actualizar_datos()
    
    def crearUI(self):
        """Crea interfaz principal moderna"""
        # Barra superior
        top_bar = ctk.CTkFrame(self, fg_color=TARJETA, height=60)
        top_bar.pack(fill=ctk.X, padx=0, pady=0)
        top_bar.pack_propagate(False)
        
        usuario = self.logica.get_usuario_actual()
        titulo = ctk.CTkLabel(top_bar, text="Sistema de Inventario",
                             font=("Segoe UI", 16, "bold"),
                             text_color=PRINCIPAL)
        titulo.pack(side=ctk.LEFT, padx=20, pady=15)
        
        user_label = ctk.CTkLabel(top_bar, text=f"Bienvenido: {usuario['nombre']}",
                                 font=("Segoe UI", 10),
                                 text_color=SECUNDARIO)
        user_label.pack(side=ctk.RIGHT, padx=20, pady=15)
        
        # Notebook (pestañas)
        self.notebook = ctk.CTkTabview(self, fg_color=FONDO,
                                       segmented_button_fg_color=SECUNDARIO,
                                       segmented_button_selected_color=PRINCIPAL,
                                       text_color=TEXTO)
        self.notebook.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        # Pestañas
        self.crear_pestaña_productos()
        self.crear_pestaña_entradas()
        self.crear_pestaña_salidas()
        self.crear_pestaña_facturas()
        self.crear_pestaña_reportes()
    
    def crear_pestaña_productos(self):
        """Crea pestaña de productos"""
        frame = self.notebook.add("Productos")
        frame.configure(fg_color=FONDO)
        
        # Tarjeta de entrada
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Crear Nuevo Producto",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        # Grid para campos
        ctk.CTkLabel(inner, text="Nombre:", text_color=TEXTO).pack(anchor="w")
        self.entrada_nombre = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_nombre.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Precio:", text_color=TEXTO).pack(anchor="w")
        self.entrada_precio = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_precio.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Stock:", text_color=TEXTO).pack(anchor="w")
        self.entrada_stock = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_stock.insert(0, "0")
        self.entrada_stock.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Stock Minimo:", text_color=TEXTO).pack(anchor="w")
        self.entrada_stock_min = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_stock_min.insert(0, "10")
        self.entrada_stock_min.pack(fill=ctk.X, pady=(0, 15))
        
        btn = ctk.CTkButton(inner, text="Crear Producto",
                           command=self.crear_producto,
                           fg_color=PRINCIPAL,
                           hover_color="#0D5C5F",
                           text_color="white",
                           height=40,
                           corner_radius=8,
                           font=("Segoe UI", 11, "bold"))
        btn.pack(fill=ctk.X)
        
        # Tarjeta de lista
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Lista de Productos",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        # Tabla simple (usando Treeview básico para ahora)
        from tkinter import ttk
        columnas = ("ID", "Nombre", "Precio", "Stock", "Estado")
        self.tabla_productos = ttk.Treeview(inner2, columns=columnas, height=12)
        
        self.tabla_productos.column("#0", width=0, stretch=False)
        for col in columnas:
            self.tabla_productos.column(col, anchor="center", width=150)
            self.tabla_productos.heading(col, text=col)
        
        self.tabla_productos.pack(fill=ctk.BOTH, expand=True)
    
    def crear_pestaña_entradas(self):
        """Crea pestaña de entradas"""
        frame = self.notebook.add("Entradas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Registrar Entrada",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(inner, text="Producto:", text_color=TEXTO).pack(anchor="w")
        self.combo_producto_entrada = ctk.CTkComboBox(inner, height=35, corner_radius=6)
        self.combo_producto_entrada.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Cantidad:", text_color=TEXTO).pack(anchor="w")
        self.entrada_cantidad_entrada = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_cantidad_entrada.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Precio Unitario:", text_color=TEXTO).pack(anchor="w")
        self.entrada_precio_entrada = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_precio_entrada.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Proveedor:", text_color=TEXTO).pack(anchor="w")
        self.entrada_proveedor = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_proveedor.pack(fill=ctk.X, pady=(0, 15))
        
        btn = ctk.CTkButton(inner, text="Registrar Entrada",
                           command=self.registrar_entrada,
                           fg_color=PRINCIPAL,
                           hover_color="#0D5C5F",
                           text_color="white",
                           height=40,
                           corner_radius=8,
                           font=("Segoe UI", 11, "bold"))
        btn.pack(fill=ctk.X)
        
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Historial de Entradas",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        from tkinter import ttk
        columnas = ("ID", "Producto", "Cantidad", "Precio", "Proveedor", "Fecha")
        self.tabla_entradas = ttk.Treeview(inner2, columns=columnas, height=10)
        
        for col in columnas:
            self.tabla_entradas.column(col, anchor="center", width=120)
            self.tabla_entradas.heading(col, text=col)
        
        self.tabla_entradas.pack(fill=ctk.BOTH, expand=True)
    
    def crear_pestaña_salidas(self):
        """Crea pestaña de salidas"""
        frame = self.notebook.add("Salidas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Registrar Salida",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(inner, text="Producto:", text_color=TEXTO).pack(anchor="w")
        self.combo_producto_salida = ctk.CTkComboBox(inner, height=35, corner_radius=6)
        self.combo_producto_salida.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Cantidad:", text_color=TEXTO).pack(anchor="w")
        self.entrada_cantidad_salida = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_cantidad_salida.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Cliente:", text_color=TEXTO).pack(anchor="w")
        self.entrada_cliente = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_cliente.pack(fill=ctk.X, pady=(0, 15))
        
        btn_frame = ctk.CTkFrame(inner, fg_color=TARJETA)
        btn_frame.pack(fill=ctk.X)
        
        btn1 = ctk.CTkButton(btn_frame, text="Salida Sin Factura",
                            command=self.registrar_salida,
                            fg_color=SECUNDARIO,
                            hover_color="#8B92A8",
                            text_color="white",
                            height=40,
                            corner_radius=8,
                            font=("Segoe UI", 10, "bold"))
        btn1.pack(side=ctk.LEFT, padx=(0, 8), fill=ctk.X, expand=True)
        
        btn2 = ctk.CTkButton(btn_frame, text="Crear Factura",
                            command=self.crear_factura_desde_salida,
                            fg_color=PRINCIPAL,
                            hover_color="#0D5C5F",
                            text_color="white",
                            height=40,
                            corner_radius=8,
                            font=("Segoe UI", 10, "bold"))
        btn2.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Historial de Salidas",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        from tkinter import ttk
        columnas = ("ID", "Producto", "Cantidad", "Cliente", "Fecha")
        self.tabla_salidas = ttk.Treeview(inner2, columns=columnas, height=10)
        
        for col in columnas:
            self.tabla_salidas.column(col, anchor="center", width=150)
            self.tabla_salidas.heading(col, text=col)
        
        self.tabla_salidas.pack(fill=ctk.BOTH, expand=True)
    
    def crear_pestaña_facturas(self):
        """Crea pestaña de facturas"""
        frame = self.notebook.add("Facturas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Nueva Factura",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(inner, text="Cliente:", text_color=TEXTO).pack(anchor="w")
        self.entrada_factura_cliente = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_factura_cliente.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="NIT:", text_color=TEXTO).pack(anchor="w")
        self.entrada_factura_nit = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_factura_nit.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Email:", text_color=TEXTO).pack(anchor="w")
        self.entrada_factura_email = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_factura_email.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner, text="Telefono:", text_color=TEXTO).pack(anchor="w")
        self.entrada_factura_telefono = ctk.CTkEntry(inner, height=35, corner_radius=6)
        self.entrada_factura_telefono.pack(fill=ctk.X, pady=(0, 15))
        
        btn = ctk.CTkButton(inner, text="Nueva Factura",
                           command=self.nueva_factura,
                           fg_color=PRINCIPAL,
                           hover_color="#0D5C5F",
                           text_color="white",
                           height=40,
                           corner_radius=8,
                           font=("Segoe UI", 11, "bold"))
        btn.pack(fill=ctk.X)
        
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.X, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Agregar Productos a Factura",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(inner2, text="Producto:", text_color=TEXTO).pack(anchor="w")
        self.combo_producto_factura = ctk.CTkComboBox(inner2, height=35, corner_radius=6)
        self.combo_producto_factura.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(inner2, text="Cantidad:", text_color=TEXTO).pack(anchor="w")
        self.entrada_cantidad_factura = ctk.CTkEntry(inner2, height=35, corner_radius=6)
        self.entrada_cantidad_factura.pack(fill=ctk.X, pady=(0, 15))
        
        btn_frame = ctk.CTkFrame(inner2, fg_color=TARJETA)
        btn_frame.pack(fill=ctk.X)
        
        btn1 = ctk.CTkButton(btn_frame, text="Agregar",
                            command=self.agregar_producto_factura,
                            fg_color=PRINCIPAL,
                            hover_color="#0D5C5F",
                            text_color="white",
                            height=35,
                            corner_radius=6,
                            font=("Segoe UI", 10, "bold"))
        btn1.pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)
        
        btn2 = ctk.CTkButton(btn_frame, text="Ver",
                            command=self.ver_factura_actual,
                            fg_color=SECUNDARIO,
                            hover_color="#8B92A8",
                            text_color="white",
                            height=35,
                            corner_radius=6,
                            font=("Segoe UI", 10, "bold"))
        btn2.pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)
        
        btn3 = ctk.CTkButton(btn_frame, text="Finalizar",
                            command=self.finalizar_factura,
                            fg_color="#DC2626",
                            hover_color="#B91C1C",
                            text_color="white",
                            height=35,
                            corner_radius=6,
                            font=("Segoe UI", 10, "bold"))
        btn3.pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        card3 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card3.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner3 = ctk.CTkFrame(card3, fg_color=TARJETA)
        inner3.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner3, text="Listado de Facturas",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        from tkinter import ttk
        columnas = ("Numero", "Cliente", "Fecha", "Total", "Estado")
        self.tabla_facturas = ttk.Treeview(inner3, columns=columnas, height=8)
        
        for col in columnas:
            self.tabla_facturas.column(col, anchor="center", width=150)
            self.tabla_facturas.heading(col, text=col)
        
        self.tabla_facturas.pack(fill=ctk.BOTH, expand=True)
        self.tabla_facturas.bind("<Double-1>", self.ver_factura_seleccionada)
    
    def crear_pestaña_reportes(self):
        """Crea pestaña de reportes"""
        frame = self.notebook.add("Reportes")
        frame.configure(fg_color=FONDO)
        
        # Estadísticas
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Estadisticas General",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.label_stats = ctk.CTkLabel(inner, text="",
                                       font=("Segoe UI", 10),
                                       text_color=TEXTO,
                                       justify="left")
        self.label_stats.pack(anchor="w", fill=ctk.X)
        
        # Bajo stock
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.X, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Productos Bajo Stock",
                    font=("Segoe UI", 12, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        from tkinter import ttk
        columnas = ("ID", "Nombre", "Stock", "Minimo")
        self.tabla_bajo_stock = ttk.Treeview(inner2, columns=columnas, height=6)
        
        for col in columnas:
            self.tabla_bajo_stock.column(col, anchor="center", width=150)
            self.tabla_bajo_stock.heading(col, text=col)
        
        self.tabla_bajo_stock.pack(fill=ctk.X)
        
        # Botón
        btn = ctk.CTkButton(frame, text="Actualizar",
                           command=self.actualizar_datos,
                           fg_color=PRINCIPAL,
                           hover_color="#0D5C5F",
                           text_color="white",
                           height=40,
                           corner_radius=8,
                           font=("Segoe UI", 11, "bold"))
        btn.pack(padx=10, pady=10, fill=ctk.X)
    
    # Métodos de funcionalidad
    def crear_producto(self):
        nombre = self.entrada_nombre.get().strip()
        precio_str = self.entrada_precio.get().strip()
        stock_str = self.entrada_stock.get().strip()
        stock_min_str = self.entrada_stock_min.get().strip()
        
        if not nombre or not precio_str:
            messagebox.showerror("Error", "Complete nombre y precio")
            return
        
        try:
            precio = float(precio_str)
            stock = int(stock_str) if stock_str else 0
            stock_min = int(stock_min_str) if stock_min_str else 10
            
            if self.logica.crear_producto(nombre, precio, stock, stock_min):
                messagebox.showinfo("Exito", "Producto creado correctamente")
                self.entrada_nombre.delete(0, ctk.END)
                self.entrada_precio.delete(0, ctk.END)
                self.entrada_stock.delete(0, ctk.END)
                self.entrada_stock.insert(0, "0")
                self.entrada_stock_min.delete(0, ctk.END)
                self.entrada_stock_min.insert(0, "10")
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo crear el producto")
        except ValueError:
            messagebox.showerror("Error", "Precio y stock deben ser numeros")
    
    def registrar_entrada(self):
        producto_id_str = self.combo_producto_entrada.get()
        cantidad_str = self.entrada_cantidad_entrada.get().strip()
        precio_str = self.entrada_precio_entrada.get().strip()
        proveedor = self.entrada_proveedor.get().strip()
        
        if not producto_id_str or not cantidad_str or not precio_str:
            messagebox.showerror("Error", "Complete todos los campos requeridos")
            return
        
        try:
            producto_id = int(producto_id_str.split(" ")[0])
            cantidad = int(cantidad_str)
            precio = float(precio_str)
            
            if self.logica.registrar_entrada(producto_id, cantidad, precio, proveedor):
                messagebox.showinfo("Exito", "Entrada registrada correctamente")
                self.entrada_cantidad_entrada.delete(0, ctk.END)
                self.entrada_precio_entrada.delete(0, ctk.END)
                self.entrada_proveedor.delete(0, ctk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo registrar la entrada")
        except ValueError:
            messagebox.showerror("Error", "Verifique cantidad y precio")
    
    def registrar_salida(self):
        producto_id_str = self.combo_producto_salida.get()
        cantidad_str = self.entrada_cantidad_salida.get().strip()
        cliente = self.entrada_cliente.get().strip()
        
        if not producto_id_str or not cantidad_str:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        try:
            producto_id = int(producto_id_str.split(" ")[0])
            cantidad = int(cantidad_str)
            
            if self.logica.registrar_salida(producto_id, cantidad, cliente):
                messagebox.showinfo("Exito", "Salida registrada correctamente")
                self.entrada_cantidad_salida.delete(0, ctk.END)
                self.entrada_cliente.delete(0, ctk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "Stock insuficiente o error en salida")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un numero")
    
    def nueva_factura(self):
        cliente = self.entrada_factura_cliente.get().strip()
        nit = self.entrada_factura_nit.get().strip()
        email = self.entrada_factura_email.get().strip()
        telefono = self.entrada_factura_telefono.get().strip()
        
        if not cliente:
            messagebox.showerror("Error", "Ingrese nombre del cliente")
            return
        
        factura_id = self.logica.crear_nueva_factura(cliente, nit, email, telefono)
        
        if factura_id:
            self.factura_actual = factura_id
            messagebox.showinfo("Exito", f"Factura creada: {factura_id}")
            self.entrada_cantidad_factura.delete(0, ctk.END)
            self.entrada_cantidad_factura.focus()
        else:
            messagebox.showerror("Error", "No se pudo crear factura")
    
    def crear_factura_desde_salida(self):
        producto_id_str = self.combo_producto_salida.get()
        cantidad_str = self.entrada_cantidad_salida.get().strip()
        cliente = self.entrada_cliente.get().strip()
        
        if not producto_id_str or not cantidad_str or not cliente:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        try:
            producto_id = int(producto_id_str.split(" ")[0])
            cantidad = int(cantidad_str)
            
            factura_id = self.logica.crear_nueva_factura(cliente)
            if not factura_id:
                messagebox.showerror("Error", "No se pudo crear factura")
                return
            
            if self.logica.agregar_producto_factura(factura_id, producto_id, cantidad):
                self.factura_actual = factura_id
                messagebox.showinfo("Exito", "Factura creada con producto")
                self.entrada_cantidad_salida.delete(0, ctk.END)
                self.entrada_cliente.delete(0, ctk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo agregar producto a factura")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un numero")
    
    def agregar_producto_factura(self):
        if not self.factura_actual:
            messagebox.showerror("Error", "Cree una factura primero")
            return
        
        producto_id_str = self.combo_producto_factura.get()
        cantidad_str = self.entrada_cantidad_factura.get().strip()
        
        if not producto_id_str or not cantidad_str:
            messagebox.showerror("Error", "Seleccione producto y cantidad")
            return
        
        try:
            producto_id = int(producto_id_str.split(" ")[0])
            cantidad = int(cantidad_str)
            
            if self.logica.agregar_producto_factura(self.factura_actual, producto_id, cantidad):
                messagebox.showinfo("Exito", "Producto agregado a factura")
                self.entrada_cantidad_factura.delete(0, ctk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo agregar producto")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un numero")
    
    def ver_factura_actual(self):
        if not self.factura_actual:
            messagebox.showerror("Error", "No hay factura abierta")
            return
        
        self.mostrar_ventana_factura(self.factura_actual)
    
    def ver_factura_seleccionada(self, event):
        seleccion = self.tabla_facturas.selection()
        if not seleccion:
            return
        
        item = seleccion[0]
        numero_factura = self.tabla_facturas.item(item)['values'][0]
        
        facturas = self.logica.obtener_facturas()
        for f in facturas:
            if f['numero_factura'] == numero_factura:
                self.mostrar_ventana_factura(f['id'])
                break
    
    def mostrar_ventana_factura(self, factura_id):
        texto_factura = self.generador_facturas.generar_texto_factura(factura_id)
        
        if not texto_factura:
            messagebox.showerror("Error", "No se pudo generar factura")
            return
        
        ventana = ctk.CTkToplevel(self)
        ventana.title("Vista de Factura")
        ventana.geometry("600x700")
        ventana.configure(fg_color=FONDO)
        
        frame = ctk.CTkFrame(ventana, fg_color=TARJETA, corner_radius=10)
        frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner = ctk.CTkFrame(frame, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        texto_widget = scrolledtext.ScrolledText(inner, wrap="word", font=("Courier", 9),
                                                bg=TARJETA, fg=TEXTO)
        texto_widget.pack(fill=ctk.BOTH, expand=True)
        texto_widget.insert("1.0", texto_factura)
        texto_widget.config(state="disabled")
        
        frame_botones = ctk.CTkFrame(ventana, fg_color=FONDO)
        frame_botones.pack(fill=ctk.X, padx=10, pady=10)
        
        factura = self.logica.obtener_factura(factura_id)
        
        btn1 = ctk.CTkButton(frame_botones, text="Guardar TXT",
                            command=lambda: self.guardar_factura_txt(factura_id),
                            fg_color=PRINCIPAL,
                            hover_color="#0D5C5F",
                            text_color="white",
                            height=35,
                            corner_radius=6)
        btn1.pack(side=ctk.LEFT, padx=5, fill=ctk.X, expand=True)
        
        btn2 = ctk.CTkButton(frame_botones, text="Guardar HTML",
                            command=lambda: self.guardar_factura_html(factura_id),
                            fg_color=PRINCIPAL,
                            hover_color="#0D5C5F",
                            text_color="white",
                            height=35,
                            corner_radius=6)
        btn2.pack(side=ctk.LEFT, padx=5, fill=ctk.X, expand=True)
        
        btn3 = ctk.CTkButton(frame_botones, text="Cerrar",
                            command=ventana.destroy,
                            fg_color=SECUNDARIO,
                            hover_color="#8B92A8",
                            text_color="white",
                            height=35,
                            corner_radius=6)
        btn3.pack(side=ctk.LEFT, padx=5, fill=ctk.X, expand=True)
    
    def guardar_factura_txt(self, factura_id):
        if self.generador_facturas.guardar_factura_txt(factura_id):
            messagebox.showinfo("Exito", "Factura guardada en Facturas/")
        else:
            messagebox.showerror("Error", "No se pudo guardar factura")
    
    def guardar_factura_html(self, factura_id):
        if self.generador_facturas.guardar_factura_html(factura_id):
            messagebox.showinfo("Exito", "Factura guardada en Facturas/")
        else:
            messagebox.showerror("Error", "No se pudo guardar factura")
    
    def finalizar_factura(self):
        if not self.factura_actual:
            messagebox.showerror("Error", "No hay factura abierta")
            return
        
        self.mostrar_ventana_factura(self.factura_actual)
        self.factura_actual = None
        messagebox.showinfo("Exito", "Factura finalizada")
        self.actualizar_datos()
    
    def actualizar_datos(self):
        """Actualiza todas las tablas y listas"""
        self.tabla_productos.delete(*self.tabla_productos.get_children())
        productos = self.logica.obtener_productos()
        
        for p in productos:
            estado = "OK" if p['stock'] >= p['stock_minimo'] else "BAJO"
            self.tabla_productos.insert("", "end", values=(
                p['id'], p['nombre'], f"${p['precio']:.2f}", 
                p['stock'], estado
            ))
        
        combo_items = [f"{p['id']} - {p['nombre']}" for p in productos]
        self.combo_producto_entrada.configure(values=combo_items)
        self.combo_producto_salida.configure(values=combo_items)
        self.combo_producto_factura.configure(values=combo_items)
        
        self.tabla_entradas.delete(*self.tabla_entradas.get_children())
        entradas = self.logica.obtener_entradas()
        for e in entradas[:10]:
            self.tabla_entradas.insert("", "end", values=(
                e['id'], e['nombre'], e['cantidad'],
                f"${e['precio_unitario']:.2f}", e['proveedor'] or "-", e['fecha'][:10]
            ))
        
        self.tabla_salidas.delete(*self.tabla_salidas.get_children())
        salidas = self.logica.obtener_salidas()
        for s in salidas[:10]:
            self.tabla_salidas.insert("", "end", values=(
                s['id'], s['nombre'], s['cantidad'], 
                s['cliente'] or "-", s['fecha'][:10]
            ))
        
        self.tabla_facturas.delete(*self.tabla_facturas.get_children())
        facturas = self.logica.obtener_facturas()
        for f in facturas:
            self.tabla_facturas.insert("", "end", values=(
                f['numero_factura'], f['cliente_nombre'],
                f['fecha'][:10], f"${f['total']:.2f}", f['estado']
            ))
        
        self.tabla_bajo_stock.delete(*self.tabla_bajo_stock.get_children())
        bajo_stock = self.logica.productos_bajo_stock()
        for p in bajo_stock:
            self.tabla_bajo_stock.insert("", "end", values=(
                p['id'], p['nombre'], p['stock'], p['stock_minimo']
            ))
        
        stats = self.logica.obtener_estadisticas()
        stats_texto = f"""Productos: {stats['total_productos']} | Entradas: {stats['total_entradas']} | Salidas: {stats['total_salidas']} | Facturas: {stats['total_facturas']}
Bajo Stock: {stats['productos_bajo_stock']} | Valor Inventario: ${stats['valor_inventario']:.2f}"""
        self.label_stats.configure(text=stats_texto)


def main():
    """Función principal"""
    ventana_login = VentanaLogin()
    ventana_login.mainloop()


if __name__ == "__main__":
    main()
