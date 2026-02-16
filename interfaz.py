"""
CAPA DE INTERFAZ - GUI con customtkinter
<<<<<<< HEAD
Aplicación de Escritorio para Inventario - Diseño Moderno
"""

import customtkinter as ctk
from tkinter import messagebox, scrolledtext
=======
Aplicacion de Escritorio para Inventario - Diseno Moderno
"""

import customtkinter as ctk
from tkinter import messagebox, scrolledtext, ttk
>>>>>>> 414289d (depuracion y correccion de bugs)
from datetime import datetime
from logica import LogicaInventario
from facturas import GeneradorFactura

<<<<<<< HEAD
# Configuración de tema
ctk.set_appearance_mode("light")

# Colores personalizados
=======
ctk.set_appearance_mode("light")

>>>>>>> 414289d (depuracion y correccion de bugs)
FONDO = "#ECEFF1"
TARJETA = "#FFFFFF"
TEXTO = "#1F2933"
PRINCIPAL = "#0F766E"
SECUNDARIO = "#9CA3AF"
ERROR = "#DC2626"

<<<<<<< HEAD
=======

class UIHelper:
    """Funciones auxiliares para creacion de widgets"""
    
    @staticmethod
    def crear_label_entrada(parent, label_text, placeholder="", is_password=False):
        """Crea label + entrada juntos"""
        ctk.CTkLabel(parent, text=label_text, font=("Segoe UI", 11, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        entrada = ctk.CTkEntry(parent, placeholder_text=placeholder, height=35,
                              corner_radius=6, show="*" if is_password else None,
                              border_width=1, border_color=SECUNDARIO, fg_color=TARJETA,
                              text_color=TEXTO)
        entrada.pack(fill=ctk.X, pady=(0, 10))
        return entrada
    
    @staticmethod
    def extraer_producto_id(combo_str):
        """Extrae ID del producto desde string 'ID - Nombre'"""
        try:
            return int(combo_str.split(" ")[0]) if combo_str else None
        except (ValueError, IndexError):
            return None
    
    @staticmethod
    def validar_int(valor_str):
        """Valida entrada como entero"""
        try:
            return int(valor_str.strip()) if valor_str.strip() else None
        except ValueError:
            return None
    
    @staticmethod
    def validar_float(valor_str):
        """Valida entrada como float"""
        try:
            return float(valor_str.strip()) if valor_str.strip() else None
        except ValueError:
            return None


>>>>>>> 414289d (depuracion y correccion de bugs)
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
            messagebox.showerror("Error de Inicializacion", 
                                f"Error al cargar la aplicacion:\n{str(e)}")
            self.destroy()
    
    def crearUI(self):
        """Crea interfaz de login moderna"""
<<<<<<< HEAD
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
=======
        main_frame = ctk.CTkFrame(self, fg_color=FONDO)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        card = ctk.CTkFrame(main_frame, fg_color=TARJETA, corner_radius=12)
        card.pack(fill=ctk.BOTH, expand=True)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(inner, text="Sistema de Inventario",
                    font=("Segoe UI", 24, "bold"), text_color=TEXTO).pack(pady=(0, 10))
        ctk.CTkLabel(inner, text="Ingrese sus credenciales",
                    font=("Segoe UI", 12), text_color=SECUNDARIO).pack(pady=(0, 25))
        
        self.entrada_usuario = UIHelper.crear_label_entrada(inner, "Usuario:", "admin")
        self.entrada_contrasena = UIHelper.crear_label_entrada(inner, "Contrasena:", "1234", 
                                                              is_password=True)
        
        btn_login = ctk.CTkButton(inner, text="INGRESAR", command=self.hacer_login,
                                 fg_color=PRINCIPAL, hover_color="#0D5C5F",
                                 text_color="white", font=("Segoe UI", 13, "bold"),
                                 height=45, corner_radius=8)
        btn_login.pack(fill=ctk.X, pady=(0, 12))
        
        btn_salir = ctk.CTkButton(inner, text="Salir", command=self.salir_app,
                                 fg_color=SECUNDARIO, hover_color="#8B92A8",
                                 text_color="white", height=40, corner_radius=8)
        btn_salir.pack(fill=ctk.X)
        
        self.entrada_usuario.focus()
        for entrada in [self.entrada_usuario, self.entrada_contrasena]:
            entrada.bind("<Return>", lambda e: self.hacer_login())
>>>>>>> 414289d (depuracion y correccion de bugs)
    
    def hacer_login(self):
        """Valida credenciales"""
        try:
            usuario = self.entrada_usuario.get().strip()
            contrasena = self.entrada_contrasena.get()
            
            if not usuario or not contrasena:
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
            if self.logica.login(usuario, contrasena):
                self.destroy()
                app = AplicacionInventario(self.logica)
                app.mainloop()
            else:
<<<<<<< HEAD
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
                self.entrada_contraseña.delete(0, ctk.END)
=======
                messagebox.showerror("Error", "Usuario o contrasena incorrectos")
                self.entrada_contrasena.delete(0, ctk.END)
>>>>>>> 414289d (depuracion y correccion de bugs)
                self.entrada_usuario.focus()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesion:\n{str(e)}")
    
    def salir_app(self):
        if messagebox.askokcancel("Salir", "Desea cerrar la aplicacion?"):
            self.destroy()


class AplicacionInventario(ctk.CTk):
<<<<<<< HEAD
    """Aplicación principal de inventario - Diseño Moderno"""
=======
    """Aplicacion principal de inventario"""
>>>>>>> 414289d (depuracion y correccion de bugs)
    
    def __init__(self, logica):
        super().__init__()
        self.title("Sistema de Inventario Local")
        self.geometry("1000x700")
        self.configure(fg_color=FONDO)
        self.logica = logica
        self.generador_facturas = GeneradorFactura(logica)
        self.factura_actual = None
<<<<<<< HEAD
=======
        self.timer_actualizacion = None
>>>>>>> 414289d (depuracion y correccion de bugs)
        
        self.crearUI()
        self.actualizar_datos()
        self.iniciar_actualizacion_automatica()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
    
    def cerrar_ventana(self):
        if self.timer_actualizacion:
            self.after_cancel(self.timer_actualizacion)
        self.destroy()
    
    def iniciar_actualizacion_automatica(self):
        self._actualizar_periodico()
    
    def _actualizar_periodico(self):
        try:
            self.actualizar_datos()
        except:
            pass
        self.timer_actualizacion = self.after(10000, self._actualizar_periodico)
    
    def crearUI(self):
<<<<<<< HEAD
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
=======
        """Crea interfaz principal"""
        top_bar = ctk.CTkFrame(self, fg_color=TARJETA, height=60)
        top_bar.pack(fill=ctk.X)
        top_bar.pack_propagate(False)
        
        usuario = self.logica.get_usuario_actual()
        ctk.CTkLabel(top_bar, text="Sistema de Inventario",
                    font=("Segoe UI", 16, "bold"), text_color=PRINCIPAL).pack(side=ctk.LEFT, padx=20, pady=15)
        
        # Boton Admin (Rojo, en la derecha)
        if self.logica.es_administrador():
            ctk.CTkButton(top_bar, text="ADMIN", command=self.abrir_panel_admin,
                         fg_color="#DC2626", hover_color="#B91C1C", text_color="white",
                         font=("Segoe UI", 12, "bold"), height=40, corner_radius=6,
                         width=100).pack(side=ctk.RIGHT, padx=10, pady=10)
        
        ctk.CTkLabel(top_bar, text=f"Bienvenido: {usuario['nombre']}",
                    font=("Segoe UI", 10), text_color=SECUNDARIO).pack(side=ctk.RIGHT, padx=20, pady=15)
        
>>>>>>> 414289d (depuracion y correccion de bugs)
        self.notebook = ctk.CTkTabview(self, fg_color=FONDO,
                                       segmented_button_fg_color=SECUNDARIO,
                                       segmented_button_selected_color=PRINCIPAL,
                                       text_color=TEXTO)
        self.notebook.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
<<<<<<< HEAD
        # Pestañas
=======
>>>>>>> 414289d (depuracion y correccion de bugs)
        self.crear_pestaña_productos()
        self.crear_pestaña_entradas()
        self.crear_pestaña_salidas()
        self.crear_pestaña_facturas()
        self.crear_pestaña_reportes()
    
    def crear_pestaña_productos(self):
<<<<<<< HEAD
        """Crea pestaña de productos"""
        frame = self.notebook.add("Productos")
        frame.configure(fg_color=FONDO)
        
        # Tarjeta de entrada
=======
        frame = self.notebook.add("Productos")
        frame.configure(fg_color=FONDO)
        
>>>>>>> 414289d (depuracion y correccion de bugs)
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Crear Nuevo Producto",
<<<<<<< HEAD
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
=======
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        self.entrada_nombre = UIHelper.crear_label_entrada(inner, "Nombre:")
        self.entrada_precio = UIHelper.crear_label_entrada(inner, "Precio:")
        self.entrada_stock = UIHelper.crear_label_entrada(inner, "Stock:")
        self.entrada_stock_min = UIHelper.crear_label_entrada(inner, "Stock Minimo:")
        
        self.entrada_stock.insert(0, "0")
>>>>>>> 414289d (depuracion y correccion de bugs)
        self.entrada_stock_min.insert(0, "10")
        self.entrada_stock_min.pack(fill=ctk.X, pady=(0, 15))
        
<<<<<<< HEAD
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
=======
        ctk.CTkButton(inner, text="Crear Producto", command=self.crear_producto,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 11, "bold")).pack(fill=ctk.X)
        
>>>>>>> 414289d (depuracion y correccion de bugs)
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Lista de Productos",
<<<<<<< HEAD
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
=======
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.tabla_productos = ttk.Treeview(inner2, columns=("ID", "Nombre", "Precio", "Stock", "Estado"), height=12)
        self.tabla_productos.column("#0", width=0, stretch=False)
        for col in ("ID", "Nombre", "Precio", "Stock", "Estado"):
            self.tabla_productos.column(col, anchor="center", width=150)
            self.tabla_productos.heading(col, text=col)
        self.tabla_productos.pack(fill=ctk.BOTH, expand=True)
        
        if self.logica.es_administrador():
            self._crear_panel_admin(frame)
    
    def _crear_panel_admin(self, frame):
        admin_card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        admin_card.pack(fill=ctk.X, padx=10, pady=10)
        
        admin_inner = ctk.CTkFrame(admin_card, fg_color=TARJETA)
        admin_inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(admin_inner, text="Modo Administrador - Gestion de Stock",
                    font=("Segoe UI", 12, "bold"), text_color="#DC2626").pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(admin_inner, text="Seleccionar Producto:", text_color=TEXTO).pack(anchor="w")
        self.combo_admin_producto = ctk.CTkComboBox(admin_inner, height=35, corner_radius=6)
        self.combo_admin_producto.pack(fill=ctk.X, pady=(0, 15))
        
        self.label_stock_actual = ctk.CTkLabel(admin_inner, text="Stock Actual: -",
                                               font=("Segoe UI", 11), text_color=TEXTO)
        self.label_stock_actual.pack(anchor="w", pady=(0, 10))
        
        btn_frame1 = ctk.CTkFrame(admin_inner, fg_color=TARJETA)
        btn_frame1.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(btn_frame1, text="Cantidad:", text_color=TEXTO).pack(side=ctk.LEFT, padx=(0, 10))
        self.entrada_admin_cantidad = ctk.CTkEntry(btn_frame1, height=35, width=100, corner_radius=6)
        self.entrada_admin_cantidad.pack(side=ctk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(btn_frame1, text="Agregar", command=self.admin_agregar_stock,
                     fg_color="#16a34a", hover_color="#15803d", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)
        
        ctk.CTkButton(btn_frame1, text="Quitar", command=self.admin_quitar_stock,
                     fg_color="#DC2626", hover_color="#B91C1C", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        btn_frame2 = ctk.CTkFrame(admin_inner, fg_color=TARJETA)
        btn_frame2.pack(fill=ctk.X)
        
        ctk.CTkLabel(btn_frame2, text="Asignar Stock:", text_color=TEXTO).pack(side=ctk.LEFT, padx=(0, 10))
        self.entrada_admin_stock_directo = ctk.CTkEntry(btn_frame2, height=35, width=100, corner_radius=6)
        self.entrada_admin_stock_directo.pack(side=ctk.LEFT, padx=(0, 10))
        
        ctk.CTkButton(btn_frame2, text="Asignar", command=self.admin_asignar_stock,
                     fg_color="#0F766E", hover_color="#0D5C5F", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, fill=ctk.X, expand=True)
    
    def crear_pestaña_entradas(self):
>>>>>>> 414289d (depuracion y correccion de bugs)
        frame = self.notebook.add("Entradas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Registrar Entrada",
<<<<<<< HEAD
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
        
=======
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(inner, text="Producto:", text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        self.combo_producto_entrada = ctk.CTkComboBox(inner, height=35, corner_radius=6)
        self.combo_producto_entrada.pack(fill=ctk.X, pady=(0, 10))
        
        self.entrada_cantidad_entrada = UIHelper.crear_label_entrada(inner, "Cantidad:")
        self.entrada_precio_entrada = UIHelper.crear_label_entrada(inner, "Precio Unitario:")
        self.entrada_proveedor = UIHelper.crear_label_entrada(inner, "Proveedor:")
        
        ctk.CTkButton(inner, text="Registrar Entrada", command=self.registrar_entrada,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 11, "bold")).pack(fill=ctk.X)
        
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
>>>>>>> 414289d (depuracion y correccion de bugs)
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Historial de Entradas",
<<<<<<< HEAD
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
=======
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.tabla_entradas = ttk.Treeview(inner2, columns=("ID", "Producto", "Cantidad", "Precio", "Proveedor", "Fecha"), height=10)
        for col in ("ID", "Producto", "Cantidad", "Precio", "Proveedor", "Fecha"):
            self.tabla_entradas.column(col, anchor="center", width=120)
            self.tabla_entradas.heading(col, text=col)
        self.tabla_entradas.pack(fill=ctk.BOTH, expand=True)
    
    def crear_pestaña_salidas(self):
>>>>>>> 414289d (depuracion y correccion de bugs)
        frame = self.notebook.add("Salidas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Registrar Salida",
<<<<<<< HEAD
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
        
=======
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(inner, text="Producto:", text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        self.combo_producto_salida = ctk.CTkComboBox(inner, height=35, corner_radius=6)
        self.combo_producto_salida.pack(fill=ctk.X, pady=(0, 10))
        
        self.entrada_cantidad_salida = UIHelper.crear_label_entrada(inner, "Cantidad:")
        self.entrada_cliente = UIHelper.crear_label_entrada(inner, "Cliente:")
        
        btn_frame = ctk.CTkFrame(inner, fg_color=TARJETA)
        btn_frame.pack(fill=ctk.X)
        
        ctk.CTkButton(btn_frame, text="Salida Sin Factura", command=self.registrar_salida,
                     fg_color=SECUNDARIO, hover_color="#8B92A8", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 10, "bold")).pack(side=ctk.LEFT, padx=(0, 8), fill=ctk.X, expand=True)
        
        ctk.CTkButton(btn_frame, text="Crear Factura", command=self.crear_factura_desde_salida,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 10, "bold")).pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
>>>>>>> 414289d (depuracion y correccion de bugs)
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
<<<<<<< HEAD
        
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
=======
        
        ctk.CTkLabel(inner2, text="Historial de Salidas",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.tabla_salidas = ttk.Treeview(inner2, columns=("ID", "Producto", "Cantidad", "Cliente", "Fecha"), height=10)
        for col in ("ID", "Producto", "Cantidad", "Cliente", "Fecha"):
            self.tabla_salidas.column(col, anchor="center", width=150)
            self.tabla_salidas.heading(col, text=col)
        self.tabla_salidas.pack(fill=ctk.BOTH, expand=True)
    
    def crear_pestaña_facturas(self):
>>>>>>> 414289d (depuracion y correccion de bugs)
        frame = self.notebook.add("Facturas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Nueva Factura",
<<<<<<< HEAD
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
        
=======
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        self.entrada_factura_cliente = UIHelper.crear_label_entrada(inner, "Cliente:")
        self.entrada_factura_nit = UIHelper.crear_label_entrada(inner, "NIT:")
        self.entrada_factura_email = UIHelper.crear_label_entrada(inner, "Email:")
        self.entrada_factura_telefono = UIHelper.crear_label_entrada(inner, "Telefono:")
        
        ctk.CTkButton(inner, text="Nueva Factura", command=self.nueva_factura,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 11, "bold")).pack(fill=ctk.X)
        
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.X, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Agregar Productos a Factura",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        ctk.CTkLabel(inner2, text="Producto:", text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        self.combo_producto_factura = ctk.CTkComboBox(inner2, height=35, corner_radius=6)
        self.combo_producto_factura.pack(fill=ctk.X, pady=(0, 10))
        
        self.entrada_cantidad_factura = UIHelper.crear_label_entrada(inner2, "Cantidad:")
        
        btn_frame = ctk.CTkFrame(inner2, fg_color=TARJETA)
        btn_frame.pack(fill=ctk.X)
        
        ctk.CTkButton(btn_frame, text="Agregar", command=self.agregar_producto_factura,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)
        
        ctk.CTkButton(btn_frame, text="Ver", command=self.ver_factura_actual,
                     fg_color=SECUNDARIO, hover_color="#8B92A8", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)
        
        ctk.CTkButton(btn_frame, text="Finalizar", command=self.finalizar_factura,
                     fg_color="#DC2626", hover_color="#B91C1C", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        card3 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card3.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner3 = ctk.CTkFrame(card3, fg_color=TARJETA)
        inner3.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner3, text="Listado de Facturas",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.tabla_facturas = ttk.Treeview(inner3, columns=("Numero", "Cliente", "Fecha", "Total", "Estado"), height=8)
        for col in ("Numero", "Cliente", "Fecha", "Total", "Estado"):
            self.tabla_facturas.column(col, anchor="center", width=150)
            self.tabla_facturas.heading(col, text=col)
>>>>>>> 414289d (depuracion y correccion de bugs)
        self.tabla_facturas.pack(fill=ctk.BOTH, expand=True)
        self.tabla_facturas.bind("<Double-1>", self.ver_factura_seleccionada)
    
    def crear_pestaña_reportes(self):
<<<<<<< HEAD
        """Crea pestaña de reportes"""
        frame = self.notebook.add("Reportes")
        frame.configure(fg_color=FONDO)
        
        # Estadísticas
=======
        frame = self.notebook.add("Reportes")
        frame.configure(fg_color=FONDO)
        
>>>>>>> 414289d (depuracion y correccion de bugs)
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Estadisticas General",
<<<<<<< HEAD
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
=======
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.label_stats = ctk.CTkLabel(inner, text="", font=("Segoe UI", 10),
                                       text_color=TEXTO, justify="left")
        self.label_stats.pack(anchor="w", fill=ctk.X)
        
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.X, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Productos Bajo Stock",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.tabla_bajo_stock = ttk.Treeview(inner2, columns=("ID", "Nombre", "Stock", "Minimo"), height=6)
        for col in ("ID", "Nombre", "Stock", "Minimo"):
>>>>>>> 414289d (depuracion y correccion de bugs)
            self.tabla_bajo_stock.column(col, anchor="center", width=150)
            self.tabla_bajo_stock.heading(col, text=col)
        self.tabla_bajo_stock.pack(fill=ctk.X)
        
<<<<<<< HEAD
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
=======
        ctk.CTkButton(frame, text="Actualizar", command=self.actualizar_datos,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 11, "bold")).pack(padx=10, pady=10, fill=ctk.X)
    
>>>>>>> 414289d (depuracion y correccion de bugs)
    def crear_producto(self):
        nombre = self.entrada_nombre.get().strip()
        precio = UIHelper.validar_float(self.entrada_precio.get())
        stock = UIHelper.validar_int(self.entrada_stock.get())
        stock_min = UIHelper.validar_int(self.entrada_stock_min.get())
        
        if not nombre or precio is None:
            messagebox.showerror("Error", "Complete nombre y precio")
            return
        
<<<<<<< HEAD
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
=======
        if stock is None or stock_min is None:
            stock = stock or 0
            stock_min = stock_min or 10
        
        if self.logica.crear_producto(nombre, precio, stock, stock_min):
            messagebox.showinfo("Exito", "Producto creado correctamente")
            self.entrada_nombre.delete(0, ctk.END)
            self.entrada_precio.delete(0, ctk.END)
            self.entrada_stock.delete(0, ctk.END)
            self.entrada_stock.insert(0, "0")
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", "No se pudo crear el producto")
    
    def actualizar_stock_admin_display(self, *args):
        producto_id = UIHelper.extraer_producto_id(self.combo_admin_producto.get())
        if not producto_id:
            self.label_stock_actual.configure(text="Stock Actual: -")
            return
        
        producto = self.logica.obtener_producto(producto_id)
        if producto:
            self.label_stock_actual.configure(text=f"Stock Actual: {producto['stock']} unidades")
    
    def admin_agregar_stock(self):
        if not self.logica.es_administrador():
            messagebox.showerror("Acceso Denegado", "Solo administrador puede modificar stock")
            return
        
        producto_id = UIHelper.extraer_producto_id(self.combo_admin_producto.get())
        cantidad = UIHelper.validar_int(self.entrada_admin_cantidad.get())
        
        if not producto_id or cantidad is None or cantidad <= 0:
            messagebox.showerror("Error", "Seleccione producto e ingrese cantidad valida")
            return
        
        if self.logica.agregar_stock_manual(producto_id, cantidad):
            messagebox.showinfo("Exito", f"Se agregaron {cantidad} unidades")
            self.entrada_admin_cantidad.delete(0, ctk.END)
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", "No se pudo agregar stock")
    
    def admin_quitar_stock(self):
        if not self.logica.es_administrador():
            messagebox.showerror("Acceso Denegado", "Solo administrador puede modificar stock")
            return
        
        producto_id = UIHelper.extraer_producto_id(self.combo_admin_producto.get())
        cantidad = UIHelper.validar_int(self.entrada_admin_cantidad.get())
        
        if not producto_id or cantidad is None or cantidad <= 0:
            messagebox.showerror("Error", "Seleccione producto e ingrese cantidad valida")
            return
        
        if self.logica.quitar_stock_manual(producto_id, cantidad):
            messagebox.showinfo("Exito", f"Se quitaron {cantidad} unidades")
            self.entrada_admin_cantidad.delete(0, ctk.END)
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", "Stock insuficiente o error en la operacion")
    
    def admin_asignar_stock(self):
        if not self.logica.es_administrador():
            messagebox.showerror("Acceso Denegado", "Solo administrador puede modificar stock")
            return
        
        producto_id = UIHelper.extraer_producto_id(self.combo_admin_producto.get())
        stock_nuevo = UIHelper.validar_int(self.entrada_admin_stock_directo.get())
        
        if not producto_id or stock_nuevo is None or stock_nuevo < 0:
            messagebox.showerror("Error", "Seleccione producto e ingrese stock valido")
            return
        
        if self.logica.cambiar_stock_manual(producto_id, stock_nuevo):
            messagebox.showinfo("Exito", f"Stock asignado a {stock_nuevo} unidades")
            self.entrada_admin_stock_directo.delete(0, ctk.END)
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", "No se pudo asignar el stock")
    
    def registrar_entrada(self):
        producto_id = UIHelper.extraer_producto_id(self.combo_producto_entrada.get())
        cantidad = UIHelper.validar_int(self.entrada_cantidad_entrada.get())
        precio = UIHelper.validar_float(self.entrada_precio_entrada.get())
>>>>>>> 414289d (depuracion y correccion de bugs)
        proveedor = self.entrada_proveedor.get().strip()
        
        if not producto_id or cantidad is None or precio is None:
            messagebox.showerror("Error", "Complete todos los campos requeridos")
            return
        
<<<<<<< HEAD
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
=======
        if self.logica.registrar_entrada(producto_id, cantidad, precio, proveedor):
            messagebox.showinfo("Exito", "Entrada registrada correctamente")
            self.entrada_cantidad_entrada.delete(0, ctk.END)
            self.entrada_precio_entrada.delete(0, ctk.END)
            self.entrada_proveedor.delete(0, ctk.END)
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", "No se pudo registrar la entrada")
    
    def registrar_salida(self):
        producto_id = UIHelper.extraer_producto_id(self.combo_producto_salida.get())
        cantidad = UIHelper.validar_int(self.entrada_cantidad_salida.get())
>>>>>>> 414289d (depuracion y correccion de bugs)
        cliente = self.entrada_cliente.get().strip()
        
        if not producto_id or cantidad is None:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
<<<<<<< HEAD
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
=======
        if self.logica.registrar_salida(producto_id, cantidad, cliente):
            messagebox.showinfo("Exito", "Salida registrada correctamente")
            self.entrada_cantidad_salida.delete(0, ctk.END)
            self.entrada_cliente.delete(0, ctk.END)
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", "Stock insuficiente o error en salida")
>>>>>>> 414289d (depuracion y correccion de bugs)
    
    def nueva_factura(self):
        cliente = self.entrada_factura_cliente.get().strip()
        
        if not cliente:
            messagebox.showerror("Error", "Ingrese nombre del cliente")
            return
        
        nit = self.entrada_factura_nit.get().strip()
        email = self.entrada_factura_email.get().strip()
        telefono = self.entrada_factura_telefono.get().strip()
        
        factura_id = self.logica.crear_nueva_factura(cliente, nit, email, telefono)
        
        if factura_id:
            self.factura_actual = factura_id
            messagebox.showinfo("Exito", f"Factura creada: {factura_id}")
            self.entrada_cantidad_factura.delete(0, ctk.END)
            self.entrada_cantidad_factura.focus()
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", "No se pudo crear factura")
    
    def crear_factura_desde_salida(self):
<<<<<<< HEAD
        producto_id_str = self.combo_producto_salida.get()
        cantidad_str = self.entrada_cantidad_salida.get().strip()
=======
        producto_id = UIHelper.extraer_producto_id(self.combo_producto_salida.get())
        cantidad = UIHelper.validar_int(self.entrada_cantidad_salida.get())
>>>>>>> 414289d (depuracion y correccion de bugs)
        cliente = self.entrada_cliente.get().strip()
        
        if not producto_id or cantidad is None or not cliente:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
<<<<<<< HEAD
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
=======
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
>>>>>>> 414289d (depuracion y correccion de bugs)
    
    def agregar_producto_factura(self):
        if not self.factura_actual:
            messagebox.showerror("Error", "Cree una factura primero")
            return
        
        producto_id = UIHelper.extraer_producto_id(self.combo_producto_factura.get())
        cantidad = UIHelper.validar_int(self.entrada_cantidad_factura.get())
        
        if not producto_id or cantidad is None:
            messagebox.showerror("Error", "Seleccione producto y cantidad")
            return
        
<<<<<<< HEAD
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
=======
        if self.logica.agregar_producto_factura(self.factura_actual, producto_id, cantidad):
            messagebox.showinfo("Exito", "Producto agregado a factura")
            self.entrada_cantidad_factura.delete(0, ctk.END)
            self.actualizar_datos()
        else:
            messagebox.showerror("Error", "No se pudo agregar producto")
>>>>>>> 414289d (depuracion y correccion de bugs)
    
    def ver_factura_actual(self):
        if not self.factura_actual:
            messagebox.showerror("Error", "No hay factura abierta")
            return
        self.mostrar_ventana_factura(self.factura_actual)
    
    def ver_factura_seleccionada(self, event):
        seleccion = self.tabla_facturas.selection()
        if not seleccion:
            return
        
<<<<<<< HEAD
        item = seleccion[0]
        numero_factura = self.tabla_facturas.item(item)['values'][0]
        
        facturas = self.logica.obtener_facturas()
        for f in facturas:
=======
        numero_factura = self.tabla_facturas.item(seleccion[0])['values'][0]
        for f in self.logica.obtener_facturas():
>>>>>>> 414289d (depuracion y correccion de bugs)
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
<<<<<<< HEAD
        
        texto_widget = scrolledtext.ScrolledText(inner, wrap="word", font=("Courier", 9),
                                                bg=TARJETA, fg=TEXTO)
        texto_widget.pack(fill=ctk.BOTH, expand=True)
        texto_widget.insert("1.0", texto_factura)
        texto_widget.config(state="disabled")
        
        frame_botones = ctk.CTkFrame(ventana, fg_color=FONDO)
        frame_botones.pack(fill=ctk.X, padx=10, pady=10)
=======
>>>>>>> 414289d (depuracion y correccion de bugs)
        
        texto_widget = scrolledtext.ScrolledText(inner, wrap="word", font=("Courier", 9),
                                                bg=TARJETA, fg=TEXTO)
        texto_widget.pack(fill=ctk.BOTH, expand=True)
        texto_widget.insert("1.0", texto_factura)
        texto_widget.config(state="disabled")
        
<<<<<<< HEAD
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
=======
        frame_botones = ctk.CTkFrame(ventana, fg_color=FONDO)
        frame_botones.pack(fill=ctk.X, padx=10, pady=10)
        
        ctk.CTkButton(frame_botones, text="Guardar TXT",
                     command=lambda: self.guardar_factura_txt(factura_id),
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=5, fill=ctk.X, expand=True)
        
        ctk.CTkButton(frame_botones, text="Guardar HTML",
                     command=lambda: self.guardar_factura_html(factura_id),
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=5, fill=ctk.X, expand=True)
        
        ctk.CTkButton(frame_botones, text="Cerrar", command=ventana.destroy,
                     fg_color=SECUNDARIO, hover_color="#8B92A8", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=5, fill=ctk.X, expand=True)
>>>>>>> 414289d (depuracion y correccion de bugs)
    
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
<<<<<<< HEAD
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
=======
        try:
            if hasattr(self, 'tabla_productos'):
                self.tabla_productos.delete(*self.tabla_productos.get_children())
                for p in self.logica.obtener_productos():
                    estado = "OK" if p['stock'] >= p['stock_minimo'] else "BAJO"
                    self.tabla_productos.insert("", "end", values=(
                        p['id'], p['nombre'], f"${p['precio']:.2f}", p['stock'], estado))
            
            productos = self.logica.obtener_productos()
            combo_items = [f"{p['id']} - {p['nombre']}" for p in productos]
            
            for combo in [getattr(self, 'combo_producto_entrada', None),
                         getattr(self, 'combo_producto_salida', None),
                         getattr(self, 'combo_producto_factura', None)]:
                if combo:
                    combo.configure(values=combo_items)
            
            if hasattr(self, 'combo_admin_producto'):
                self.combo_admin_producto.configure(values=combo_items)
                self.combo_admin_producto.bind("<FocusOut>", self.actualizar_stock_admin_display)
                if self.combo_admin_producto.get():
                    self.actualizar_stock_admin_display()
            
            if hasattr(self, 'tabla_entradas'):
                self.tabla_entradas.delete(*self.tabla_entradas.get_children())
                for e in self.logica.obtener_entradas()[:10]:
                    self.tabla_entradas.insert("", "end", values=(
                        e['id'], e['nombre'], e['cantidad'],
                        f"${e['precio_unitario']:.2f}", e['proveedor'] or "-", e['fecha'][:10]))
            
            if hasattr(self, 'tabla_salidas'):
                self.tabla_salidas.delete(*self.tabla_salidas.get_children())
                for s in self.logica.obtener_salidas()[:10]:
                    self.tabla_salidas.insert("", "end", values=(
                        s['id'], s['nombre'], s['cantidad'], 
                        s['cliente'] or "-", s['fecha'][:10]))
            
            if hasattr(self, 'tabla_facturas'):
                self.tabla_facturas.delete(*self.tabla_facturas.get_children())
                for f in self.logica.obtener_facturas():
                    self.tabla_facturas.insert("", "end", values=(
                        f['numero_factura'], f['cliente_nombre'],
                        f['fecha'][:10], f"${f['total']:.2f}", f['estado']))
            
            if hasattr(self, 'tabla_bajo_stock'):
                self.tabla_bajo_stock.delete(*self.tabla_bajo_stock.get_children())
                for p in self.logica.productos_bajo_stock():
                    self.tabla_bajo_stock.insert("", "end", values=(
                        p['id'], p['nombre'], p['stock'], p['stock_minimo']))
            
            if hasattr(self, 'label_stats'):
                stats = self.logica.obtener_estadisticas()
                stats_texto = f"""Productos: {stats['total_productos']} | Entradas: {stats['total_entradas']} | Salidas: {stats['total_salidas']} | Facturas: {stats['total_facturas']}
Bajo Stock: {stats['productos_bajo_stock']} | Valor Inventario: ${stats['valor_inventario']:.2f}"""
                self.label_stats.configure(text=stats_texto)
        except Exception:
            pass
    
    def abrir_panel_admin(self):
        """Abre panel de administrador con verificacion de contrasena"""
        # Crear ventana de autenticacion
        ventana_auth = ctk.CTkToplevel(self)
        ventana_auth.title("Verificacion de Administrador")
        ventana_auth.geometry("400x250")
        ventana_auth.configure(fg_color=FONDO)
        ventana_auth.resizable(False, False)
        
        # Hacer ventana modal
        ventana_auth.transient(self)
        ventana_auth.grab_set()
        
        frame = ctk.CTkFrame(ventana_auth, fg_color=TARJETA, corner_radius=12)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        inner = ctk.CTkFrame(frame, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(inner, text="PANEL ADMINISTRATIVO",
                    font=("Segoe UI", 14, "bold"), text_color="#DC2626").pack(pady=(0, 20))
        
        ctk.CTkLabel(inner, text="Contrasena para verificacion:",
                    font=("Segoe UI", 11, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        
        entrada_pass = ctk.CTkEntry(inner, placeholder_text="Ingrese contrasena", 
                                   show="*", height=35, corner_radius=6)
        entrada_pass.pack(fill=ctk.X, pady=(0, 20))
        entrada_pass.focus()
        
        def verificar():
            try:
                contrasena = entrada_pass.get()
                # Obtener nombre de usuario del usuario actual
                usuario_actual = self.logica.usuario_actual.get('usuario') if self.logica.usuario_actual else None
                
                if not usuario_actual:
                    messagebox.showerror("Error", "No hay usuario activo")
                    return
                
                # Verificar credenciales del usuario actual
                if self.logica.login(usuario_actual, contrasena):
                    ventana_auth.destroy()
                    self.mostrar_panel_edicion()
                else:
                    messagebox.showerror("Error", "Contrasena incorrecta")
                    entrada_pass.delete(0, ctk.END)
                    entrada_pass.focus()
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar: {str(e)}")
        
        btn_frame = ctk.CTkFrame(inner, fg_color=TARJETA)
        btn_frame.pack(fill=ctk.X)
        
        ctk.CTkButton(btn_frame, text="Verificar", command=verificar,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 11, "bold")).pack(side=ctk.LEFT, padx=(0, 10), fill=ctk.X, expand=True)
        
        ctk.CTkButton(btn_frame, text="Cancelar", command=ventana_auth.destroy,
                     fg_color=SECUNDARIO, hover_color="#8B92A8", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 11, "bold")).pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        entrada_pass.bind("<Return>", lambda e: verificar())
    
    def mostrar_panel_edicion(self):
        """Muestra panel para editar base de datos de productos"""
        ventana = ctk.CTkToplevel(self)
        ventana.title("ADMINISTRADOR - Edicion de Productos")
        ventana.geometry("900x700")
        ventana.configure(fg_color=FONDO)
        
        # Barra superior
        top = ctk.CTkFrame(ventana, fg_color="#DC2626", height=50)
        top.pack(fill=ctk.X)
        top.pack_propagate(False)
        
        ctk.CTkLabel(top, text="PANEL DE ADMINISTRADOR - Gestionar Productos",
                    font=("Segoe UI", 14, "bold"), text_color="white").pack(pady=12)
        
        # Frame principal
        main_frame = ctk.CTkFrame(ventana, fg_color=FONDO)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        # Seccion: Crear/Editar producto
        card1 = ctk.CTkFrame(main_frame, fg_color=TARJETA, corner_radius=10)
        card1.pack(fill=ctk.X, pady=(0, 10))
        
        inner1 = ctk.CTkFrame(card1, fg_color=TARJETA)
        inner1.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner1, text="Crear o Editar Producto",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        # Campos de entrada
        ctk.CTkLabel(inner1, text="ID/Nombre del Producto:", text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        
        combo_productos = ctk.CTkComboBox(inner1, height=35, corner_radius=6)
        combo_productos.pack(fill=ctk.X, pady=(0, 10))
        
        entrada_nombre = UIHelper.crear_label_entrada(inner1, "Nombre:")
        entrada_precio = UIHelper.crear_label_entrada(inner1, "Precio:")
        entrada_stock = UIHelper.crear_label_entrada(inner1, "Stock:")
        entrada_stock_min = UIHelper.crear_label_entrada(inner1, "Stock Minimo:")
        
        ctk.CTkLabel(inner1, text="Descripcion:", font=("Segoe UI", 11, "bold"),
                    text_color=TEXTO).pack(anchor="w", pady=(0, 5))
        entrada_descripcion = ctk.CTkTextbox(inner1, height=80, corner_radius=6)
        entrada_descripcion.pack(fill=ctk.X, pady=(0, 15))
        
        def cargar_producto():
            """Carga datos del producto seleccionado"""
            producto_id = UIHelper.extraer_producto_id(combo_productos.get())
            if not producto_id:
                return
            
            producto = self.logica.obtener_producto(producto_id)
            if producto:
                entrada_nombre.delete(0, ctk.END)
                entrada_nombre.insert(0, producto['nombre'])
                entrada_precio.delete(0, ctk.END)
                entrada_precio.insert(0, str(producto['precio']))
                entrada_stock.delete(0, ctk.END)
                entrada_stock.insert(0, str(producto['stock']))
                entrada_stock_min.delete(0, ctk.END)
                entrada_stock_min.insert(0, str(producto['stock_minimo']))
                entrada_descripcion.delete("1.0", ctk.END)
                entrada_descripcion.insert("1.0", producto.get('descripcion') or "")
        
        def guardar_cambios():
            """Guarda cambios en la BD"""
            producto_id = UIHelper.extraer_producto_id(combo_productos.get())
            nombre = entrada_nombre.get().strip()
            precio = UIHelper.validar_float(entrada_precio.get())
            stock = UIHelper.validar_int(entrada_stock.get())
            stock_min = UIHelper.validar_int(entrada_stock_min.get())
            descripcion = entrada_descripcion.get("1.0", ctk.END).strip()
            
            if not nombre or precio is None or stock is None or stock_min is None:
                messagebox.showerror("Error", "Complete todos los campos requeridos")
                return
            
            if producto_id:
                # Actualizar producto existente
                try:
                    conn = self.logica.db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute('''UPDATE productos 
                                    SET nombre=?, precio=?, stock=?, stock_minimo=?, descripcion=?
                                    WHERE id=?''',
                                  (nombre, precio, stock, stock_min, descripcion, producto_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Exito", "Producto actualizado correctamente")
                    self.actualizar_datos()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
            else:
                # Crear nuevo producto
                if self.logica.crear_producto(nombre, precio, stock, stock_min, descripcion):
                    messagebox.showinfo("Exito", "Producto creado correctamente")
                    entrada_nombre.delete(0, ctk.END)
                    entrada_precio.delete(0, ctk.END)
                    entrada_stock.delete(0, ctk.END)
                    entrada_stock_min.delete(0, ctk.END)
                    entrada_descripcion.delete("1.0", ctk.END)
                    self.actualizar_datos()
                    actualizar_combo()
                else:
                    messagebox.showerror("Error", "No se pudo crear el producto")
        
        def actualizar_combo():
            """Actualiza lista de productos en combo"""
            productos = self.logica.obtener_productos()
            combo_items = [f"{p['id']} - {p['nombre']}" for p in productos]
            combo_productos.configure(values=combo_items)
        
        combo_productos.bind("<FocusOut>", lambda e: cargar_producto())
        actualizar_combo()
        
        btn_frame1 = ctk.CTkFrame(inner1, fg_color=TARJETA)
        btn_frame1.pack(fill=ctk.X)
        
        ctk.CTkButton(btn_frame1, text="Cargar Producto", command=cargar_producto,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)
        
        ctk.CTkButton(btn_frame1, text="Guardar Cambios", command=guardar_cambios,
                     fg_color="#16a34a", hover_color="#15803d", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)
        
        ctk.CTkButton(btn_frame1, text="Limpiar", command=lambda: [
                     entrada_nombre.delete(0, ctk.END),
                     entrada_precio.delete(0, ctk.END),
                     entrada_stock.delete(0, ctk.END),
                     entrada_stock_min.delete(0, ctk.END),
                     entrada_descripcion.delete("1.0", ctk.END),
                     combo_productos.set("")
                     ],
                     fg_color=SECUNDARIO, hover_color="#8B92A8", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, fill=ctk.X, expand=True)
        
        # Seccion: Tabla de productos actuales
        card2 = ctk.CTkFrame(main_frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, pady=(10, 0))
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Productos en Base de Datos",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        tabla_admin = ttk.Treeview(inner2, columns=("ID", "Nombre", "Precio", "Stock", "Stock Min", "Descripcion"), height=15)
        tabla_admin.column("#0", width=0, stretch=False)
        for col in ("ID", "Nombre", "Precio", "Stock", "Stock Min", "Descripcion"):
            tabla_admin.column(col, anchor="center", width=120)
            tabla_admin.heading(col, text=col)
        
        tabla_admin.pack(fill=ctk.BOTH, expand=True, pady=(0, 10))
        
        def actualizar_tabla():
            tabla_admin.delete(*tabla_admin.get_children())
            for p in self.logica.obtener_productos():
                tabla_admin.insert("", "end", values=(
                    p['id'], p['nombre'], f"${p['precio']:.2f}", 
                    p['stock'], p['stock_minimo'], p.get('descripcion', '')[:30]))
        
        def eliminar_producto():
            """Elimina producto seleccionado"""
            seleccion = tabla_admin.selection()
            if not seleccion:
                messagebox.showerror("Error", "Seleccione un producto para eliminar")
                return
            
            producto_id = tabla_admin.item(seleccion[0])['values'][0]
            if messagebox.askyesno("Confirmar", "¿Desea eliminar este producto?"):
                try:
                    conn = self.logica.db.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM productos WHERE id=?", (producto_id,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Exito", "Producto eliminado")
                    actualizar_tabla()
                    actualizar_combo()
                    self.actualizar_datos()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
        
        actualizar_tabla()
        
        btn_frame2 = ctk.CTkFrame(inner2, fg_color=TARJETA)
        btn_frame2.pack(fill=ctk.X)
        
        ctk.CTkButton(btn_frame2, text="Recargar", command=actualizar_tabla,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)
        
        ctk.CTkButton(btn_frame2, text="Eliminar Seleccionado", command=eliminar_producto,
                     fg_color="#DC2626", hover_color="#B91C1C", text_color="white",
                     height=35, corner_radius=6).pack(side=ctk.LEFT, fill=ctk.X, expand=True)
>>>>>>> 414289d (depuracion y correccion de bugs)


def main():
    """Punto de entrada de la aplicación"""
    ventana_login = VentanaLogin()
    ventana_login.mainloop()


if __name__ == "__main__":
    main()

