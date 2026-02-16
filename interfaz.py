"""
CAPA DE INTERFAZ - GUI con customtkinter
Aplicacion de Escritorio para Inventario - Diseno Moderno
VERSION MEJORADA: Búsqueda en tiempo real + Carga automática + Correcciones
"""

import customtkinter as ctk
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime
from logica import LogicaInventario
from facturas import GeneradorFactura
import logging

# Configurar logging para mejor debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ctk.set_appearance_mode("light")

FONDO = "#ECEFF1"
TARJETA = "#FFFFFF"
TEXTO = "#1F2933"
PRINCIPAL = "#0F766E"
SECUNDARIO = "#9CA3AF"
ERROR = "#DC2626"


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
                messagebox.showerror("Error", "Usuario o contrasena incorrectos")
                self.entrada_contrasena.delete(0, ctk.END)
                self.entrada_usuario.focus()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesion:\n{str(e)}")
    
    def salir_app(self):
        if messagebox.askokcancel("Salir", "Desea cerrar la aplicacion?"):
            self.destroy()


class AplicacionInventario(ctk.CTk):
    """Aplicacion principal de inventario"""
    
    def __init__(self, logica):
        super().__init__()
        self.title("Sistema de Inventario Local")
        self.geometry("1000x700")
        self.configure(fg_color=FONDO)
        self.logica = logica
        self.generador_facturas = GeneradorFactura(logica)
        self.factura_actual = None
        
        # ✅ CORRECCIÓN N4: Inicializar timer SIEMPRE (antes era None solo a veces)
        self.timer_actualizacion = None
        
        self.crearUI()
        
        # ✅ MEJORA: Carga inicial de datos (doble llamada para asegurar)
        self.actualizar_datos()
        self.after(200, self.actualizar_datos)  # Segunda carga tras 200ms
        
        self.iniciar_actualizacion_automatica()
        self.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
    
    def cerrar_ventana(self):
        """Cierre seguro con cancelación de timer"""
        # ✅ CORRECCIÓN N4: Verificación más robusta
        if hasattr(self, 'timer_actualizacion') and self.timer_actualizacion:
            try:
                self.after_cancel(self.timer_actualizacion)
                logging.info("Timer de actualización cancelado correctamente")
            except Exception as e:
                logging.warning(f"Error al cancelar timer: {e}")
        self.destroy()
    
    def iniciar_actualizacion_automatica(self):
        """Inicia actualizaciones periódicas"""
        self._actualizar_periodico()
    
    def _actualizar_periodico(self):
        """Actualización periódica con mejor manejo de errores"""
        # ✅ CORRECCIÓN N3: Ya no usa except: pass
        try:
            self.actualizar_datos()
        except Exception as e:
            # Registrar error pero continuar funcionando
            logging.error(f"Error al actualizar datos periódicamente: {e}")
            # No mostrar popup para no molestar al usuario constantemente
        
        # Programar siguiente actualización
        self.timer_actualizacion = self.after(10000, self._actualizar_periodico)
    
    def crearUI(self):
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
        
        self.notebook = ctk.CTkTabview(self, fg_color=FONDO,
                                       segmented_button_fg_color=SECUNDARIO,
                                       segmented_button_selected_color=PRINCIPAL,
                                       text_color=TEXTO)
        self.notebook.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        self.crear_pestaña_productos()
        self.crear_pestaña_entradas()
        self.crear_pestaña_salidas()
        self.crear_pestaña_facturas()
        self.crear_pestaña_reportes()
    
    def crear_pestaña_productos(self):
        frame = self.notebook.add("Productos")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Crear Nuevo Producto",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 15))
        
        self.entrada_nombre = UIHelper.crear_label_entrada(inner, "Nombre:")
        self.entrada_precio = UIHelper.crear_label_entrada(inner, "Precio:")
        self.entrada_stock = UIHelper.crear_label_entrada(inner, "Stock:")
        self.entrada_stock_min = UIHelper.crear_label_entrada(inner, "Stock Minimo:")
        
        self.entrada_stock.insert(0, "0")
        self.entrada_stock_min.insert(0, "10")
        
        ctk.CTkButton(inner, text="Crear Producto", command=self.crear_producto,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 11, "bold")).pack(fill=ctk.X)
        
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Lista de Productos",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        # ✅ NUEVO: Frame de búsqueda
        search_frame = ctk.CTkFrame(inner2, fg_color=TARJETA)
        search_frame.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(search_frame, text="🔍 Buscar:", font=("Segoe UI", 11),
                    text_color=TEXTO).pack(side=ctk.LEFT, padx=(0, 10))
        
        self.entrada_buscar_producto = ctk.CTkEntry(search_frame, 
                                                    placeholder_text="Nombre del producto...",
                                                    height=35, corner_radius=6)
        self.entrada_buscar_producto.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 10))
        
        # ✅ NUEVO: Búsqueda en tiempo real
        self.entrada_buscar_producto.bind("<KeyRelease>", self.filtrar_productos)
        
        ctk.CTkButton(search_frame, text="Limpiar", command=self.limpiar_busqueda_productos,
                     fg_color=SECUNDARIO, hover_color="#8B92A8", text_color="white",
                     height=35, corner_radius=6, width=100).pack(side=ctk.LEFT)
        
        self.tabla_productos = ttk.Treeview(inner2, columns=("ID", "Nombre", "Precio", "Stock", "Estado"), height=12)
        self.tabla_productos.column("#0", width=0, stretch=False)
        for col in ("ID", "Nombre", "Precio", "Stock", "Estado"):
            self.tabla_productos.column(col, anchor="center", width=150)
            self.tabla_productos.heading(col, text=col)
        self.tabla_productos.pack(fill=ctk.BOTH, expand=True)
        
        if self.logica.es_administrador():
            self._crear_panel_admin(frame)
    
    # ✅ NUEVO: Métodos de búsqueda de productos
    def filtrar_productos(self, event=None):
        """Filtra productos según búsqueda en tiempo real"""
        try:
            busqueda = self.entrada_buscar_producto.get().lower().strip()
            
            # Limpiar tabla
            self.tabla_productos.delete(*self.tabla_productos.get_children())
            
            # Obtener todos los productos
            productos = self.logica.obtener_productos()
            
            # Filtrar por búsqueda
            if busqueda:
                productos = [p for p in productos if busqueda in p['nombre'].lower()]
            
            # ✅ NUEVO: Ordenar alfabéticamente por nombre
            productos = sorted(productos, key=lambda p: p['nombre'].lower())
            
            # Mostrar productos filtrados
            for p in productos:
                estado = "OK" if p['stock'] >= p['stock_minimo'] else "BAJO"
                self.tabla_productos.insert("", "end", values=(
                    p['id'], p['nombre'], f"${p['precio']:.2f}", p['stock'], estado))
        except Exception as e:
            logging.error(f"Error al filtrar productos: {e}")
    
    def limpiar_busqueda_productos(self):
        """Limpia búsqueda y muestra todos los productos"""
        self.entrada_buscar_producto.delete(0, ctk.END)
        self.actualizar_datos()
    
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
        frame = self.notebook.add("Entradas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Registrar Entrada",
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
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Historial de Entradas",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.tabla_entradas = ttk.Treeview(inner2, columns=("ID", "Producto", "Cantidad", "Precio", "Proveedor", "Fecha"), height=10)
        self.tabla_entradas.column("#0", width=0, stretch=False)
        for col in ("ID", "Producto", "Cantidad", "Precio", "Proveedor", "Fecha"):
            self.tabla_entradas.column(col, anchor="center", width=120)
            self.tabla_entradas.heading(col, text=col)
        self.tabla_entradas.pack(fill=ctk.BOTH, expand=True)
    
    def crear_pestaña_salidas(self):
        frame = self.notebook.add("Salidas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Registrar Salida",
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
        
        card2 = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card2.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        inner2 = ctk.CTkFrame(card2, fg_color=TARJETA)
        inner2.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(inner2, text="Historial de Salidas",
                    font=("Segoe UI", 12, "bold"), text_color=TEXTO).pack(anchor="w", pady=(0, 10))
        
        self.tabla_salidas = ttk.Treeview(inner2, columns=("ID", "Producto", "Cantidad", "Cliente", "Fecha"), height=10)
        self.tabla_salidas.column("#0", width=0, stretch=False)
        for col in ("ID", "Producto", "Cantidad", "Cliente", "Fecha"):
            self.tabla_salidas.column(col, anchor="center", width=150)
            self.tabla_salidas.heading(col, text=col)
        self.tabla_salidas.pack(fill=ctk.BOTH, expand=True)
    
    def crear_pestaña_facturas(self):
        frame = self.notebook.add("Facturas")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Nueva Factura",
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
        self.tabla_facturas.column("#0", width=0, stretch=False)
        for col in ("Numero", "Cliente", "Fecha", "Total", "Estado"):
            self.tabla_facturas.column(col, anchor="center", width=150)
            self.tabla_facturas.heading(col, text=col)
        self.tabla_facturas.pack(fill=ctk.BOTH, expand=True)
        self.tabla_facturas.bind("<Double-1>", self.ver_factura_seleccionada)
    
    def crear_pestaña_reportes(self):
        frame = self.notebook.add("Reportes")
        frame.configure(fg_color=FONDO)
        
        card = ctk.CTkFrame(frame, fg_color=TARJETA, corner_radius=10)
        card.pack(fill=ctk.X, padx=10, pady=10)
        
        inner = ctk.CTkFrame(card, fg_color=TARJETA)
        inner.pack(fill=ctk.BOTH, padx=15, pady=15)
        
        ctk.CTkLabel(inner, text="Estadisticas General",
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
        self.tabla_bajo_stock.column("#0", width=0, stretch=False)
        for col in ("ID", "Nombre", "Stock", "Minimo"):
            self.tabla_bajo_stock.column(col, anchor="center", width=150)
            self.tabla_bajo_stock.heading(col, text=col)
        self.tabla_bajo_stock.pack(fill=ctk.X)
        
        ctk.CTkButton(frame, text="Actualizar", command=self.actualizar_datos,
                     fg_color=PRINCIPAL, hover_color="#0D5C5F", text_color="white",
                     height=40, corner_radius=8, font=("Segoe UI", 11, "bold")).pack(padx=10, pady=10, fill=ctk.X)
    
    def crear_producto(self):
        """Crea un nuevo producto"""
        try:
            nombre = self.entrada_nombre.get().strip()
            precio = UIHelper.validar_float(self.entrada_precio.get())
            stock = UIHelper.validar_int(self.entrada_stock.get())
            stock_min = UIHelper.validar_int(self.entrada_stock_min.get())
            
            if not nombre or precio is None:
                messagebox.showerror("Error", "Complete nombre y precio")
                return
            
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
        except Exception as e:
            logging.error(f"Error al crear producto: {e}")
            messagebox.showerror("Error", f"Error al crear producto: {str(e)}")
    
    def actualizar_stock_admin_display(self, *args):
        """Actualiza el display del stock actual en panel admin"""
        try:
            producto_id = UIHelper.extraer_producto_id(self.combo_admin_producto.get())
            if not producto_id:
                self.label_stock_actual.configure(text="Stock Actual: -")
                return
            
            producto = self.logica.obtener_producto(producto_id)
            if producto:
                self.label_stock_actual.configure(text=f"Stock Actual: {producto['stock']} unidades")
        except Exception as e:
            logging.error(f"Error al actualizar display de stock: {e}")
    
    def admin_agregar_stock(self):
        """Agrega stock manualmente (solo admin)"""
        try:
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
        except Exception as e:
            logging.error(f"Error al agregar stock: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def admin_quitar_stock(self):
        """Quita stock manualmente (solo admin)"""
        try:
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
        except Exception as e:
            logging.error(f"Error al quitar stock: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def admin_asignar_stock(self):
        """Asigna stock directamente (solo admin)"""
        try:
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
        except Exception as e:
            logging.error(f"Error al asignar stock: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def registrar_entrada(self):
        """Registra una entrada de producto"""
        try:
            producto_id = UIHelper.extraer_producto_id(self.combo_producto_entrada.get())
            cantidad = UIHelper.validar_int(self.entrada_cantidad_entrada.get())
            precio = UIHelper.validar_float(self.entrada_precio_entrada.get())
            proveedor = self.entrada_proveedor.get().strip()
            
            if not producto_id or cantidad is None or precio is None:
                messagebox.showerror("Error", "Complete todos los campos requeridos")
                return
            
            if self.logica.registrar_entrada(producto_id, cantidad, precio, proveedor):
                messagebox.showinfo("Exito", "Entrada registrada correctamente")
                self.entrada_cantidad_entrada.delete(0, ctk.END)
                self.entrada_precio_entrada.delete(0, ctk.END)
                self.entrada_proveedor.delete(0, ctk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo registrar la entrada")
        except Exception as e:
            logging.error(f"Error al registrar entrada: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def registrar_salida(self):
        """Registra una salida de producto"""
        try:
            producto_id = UIHelper.extraer_producto_id(self.combo_producto_salida.get())
            cantidad = UIHelper.validar_int(self.entrada_cantidad_salida.get())
            cliente = self.entrada_cliente.get().strip()
            
            if not producto_id or cantidad is None:
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
            if self.logica.registrar_salida(producto_id, cantidad, cliente):
                messagebox.showinfo("Exito", "Salida registrada correctamente")
                self.entrada_cantidad_salida.delete(0, ctk.END)
                self.entrada_cliente.delete(0, ctk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "Stock insuficiente o error en salida")
        except Exception as e:
            logging.error(f"Error al registrar salida: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def nueva_factura(self):
        """Crea una nueva factura"""
        try:
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
        except Exception as e:
            logging.error(f"Error al crear factura: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def crear_factura_desde_salida(self):
        """Crea factura directamente desde una salida"""
        try:
            producto_id = UIHelper.extraer_producto_id(self.combo_producto_salida.get())
            cantidad = UIHelper.validar_int(self.entrada_cantidad_salida.get())
            cliente = self.entrada_cliente.get().strip()
            
            if not producto_id or cantidad is None or not cliente:
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
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
        except Exception as e:
            logging.error(f"Error al crear factura desde salida: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def agregar_producto_factura(self):
        """Agrega un producto a la factura actual"""
        try:
            if not self.factura_actual:
                messagebox.showerror("Error", "Cree una factura primero")
                return
            
            producto_id = UIHelper.extraer_producto_id(self.combo_producto_factura.get())
            cantidad = UIHelper.validar_int(self.entrada_cantidad_factura.get())
            
            if not producto_id or cantidad is None:
                messagebox.showerror("Error", "Seleccione producto y cantidad")
                return
            
            if self.logica.agregar_producto_factura(self.factura_actual, producto_id, cantidad):
                messagebox.showinfo("Exito", "Producto agregado a factura")
                self.entrada_cantidad_factura.delete(0, ctk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo agregar producto")
        except Exception as e:
            logging.error(f"Error al agregar producto a factura: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def ver_factura_actual(self):
        """Muestra la factura actualmente abierta"""
        if not self.factura_actual:
            messagebox.showerror("Error", "No hay factura abierta")
            return
        self.mostrar_ventana_factura(self.factura_actual)
    
    def ver_factura_seleccionada(self, event):
        """Muestra factura seleccionada desde la tabla"""
        try:
            seleccion = self.tabla_facturas.selection()
            if not seleccion:
                return
            
            numero_factura = self.tabla_facturas.item(seleccion[0])['values'][0]
            for f in self.logica.obtener_facturas():
                if f['numero_factura'] == numero_factura:
                    self.mostrar_ventana_factura(f['id'])
                    break
        except Exception as e:
            logging.error(f"Error al ver factura seleccionada: {e}")
    
    def mostrar_ventana_factura(self, factura_id):
        """Muestra ventana con la factura"""
        try:
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
        except Exception as e:
            logging.error(f"Error al mostrar ventana de factura: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def guardar_factura_txt(self, factura_id):
        """Guarda factura en formato TXT"""
        try:
            if self.generador_facturas.guardar_factura_txt(factura_id):
                messagebox.showinfo("Exito", "Factura guardada en Facturas/")
            else:
                messagebox.showerror("Error", "No se pudo guardar factura")
        except Exception as e:
            logging.error(f"Error al guardar factura TXT: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def guardar_factura_html(self, factura_id):
        """Guarda factura en formato HTML"""
        try:
            if self.generador_facturas.guardar_factura_html(factura_id):
                messagebox.showinfo("Exito", "Factura guardada en Facturas/")
            else:
                messagebox.showerror("Error", "No se pudo guardar factura")
        except Exception as e:
            logging.error(f"Error al guardar factura HTML: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def finalizar_factura(self):
        """Finaliza y cierra la factura actual"""
        try:
            if not self.factura_actual:
                messagebox.showerror("Error", "No hay factura abierta")
                return
            
            self.mostrar_ventana_factura(self.factura_actual)
            self.factura_actual = None
            messagebox.showinfo("Exito", "Factura finalizada")
            self.actualizar_datos()
        except Exception as e:
            logging.error(f"Error al finalizar factura: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def actualizar_datos(self):
        """Actualiza todas las tablas y listas con mejor manejo de errores"""
        try:
            # Actualizar tabla de productos
            if hasattr(self, 'tabla_productos'):
                self.tabla_productos.delete(*self.tabla_productos.get_children())
                
                # ✅ NUEVO: Obtener y ordenar alfabéticamente
                productos = self.logica.obtener_productos()
                productos = sorted(productos, key=lambda p: p['nombre'].lower())
                
                for p in productos:
                    estado = "OK" if p['stock'] >= p['stock_minimo'] else "BAJO"
                    self.tabla_productos.insert("", "end", values=(
                        p['id'], p['nombre'], f"${p['precio']:.2f}", p['stock'], estado))
            
            # Actualizar combos de productos
            productos = self.logica.obtener_productos()
            combo_items = [f"{p['id']} - {p['nombre']}" for p in productos]
            
            for combo in [getattr(self, 'combo_producto_entrada', None),
                         getattr(self, 'combo_producto_salida', None),
                         getattr(self, 'combo_producto_factura', None)]:
                if combo:
                    combo.configure(values=combo_items)
            
            # Actualizar combo admin
            if hasattr(self, 'combo_admin_producto'):
                self.combo_admin_producto.configure(values=combo_items)
                self.combo_admin_producto.bind("<<ComboboxSelected>>", self.actualizar_stock_admin_display)
                if self.combo_admin_producto.get():
                    self.actualizar_stock_admin_display()
            
            # Actualizar tabla de entradas
            if hasattr(self, 'tabla_entradas'):
                self.tabla_entradas.delete(*self.tabla_entradas.get_children())
                for e in self.logica.obtener_entradas()[:10]:
                    self.tabla_entradas.insert("", "end", values=(
                        e['id'], e['nombre'], e['cantidad'],
                        f"${e['precio_unitario']:.2f}", e['proveedor'] or "-", e['fecha'][:10]))
            
            # Actualizar tabla de salidas
            if hasattr(self, 'tabla_salidas'):
                self.tabla_salidas.delete(*self.tabla_salidas.get_children())
                for s in self.logica.obtener_salidas()[:10]:
                    self.tabla_salidas.insert("", "end", values=(
                        s['id'], s['nombre'], s['cantidad'], 
                        s['cliente'] or "-", s['fecha'][:10]))
            
            # Actualizar tabla de facturas
            if hasattr(self, 'tabla_facturas'):
                self.tabla_facturas.delete(*self.tabla_facturas.get_children())
                for f in self.logica.obtener_facturas():
                    self.tabla_facturas.insert("", "end", values=(
                        f['numero_factura'], f['cliente_nombre'],
                        f['fecha'][:10], f"${f['total']:.2f}", f['estado']))
            
            # Actualizar tabla bajo stock
            if hasattr(self, 'tabla_bajo_stock'):
                self.tabla_bajo_stock.delete(*self.tabla_bajo_stock.get_children())
                for p in self.logica.productos_bajo_stock():
                    self.tabla_bajo_stock.insert("", "end", values=(
                        p['id'], p['nombre'], p['stock'], p['stock_minimo']))
            
            # Actualizar estadísticas
            if hasattr(self, 'label_stats'):
                stats = self.logica.obtener_estadisticas()
                stats_texto = f"""Productos: {stats['total_productos']} | Entradas: {stats['total_entradas']} | Salidas: {stats['total_salidas']} | Facturas: {stats['total_facturas']}
Bajo Stock: {stats['productos_bajo_stock']} | Valor Inventario: ${stats['valor_inventario']:.2f}"""
                self.label_stats.configure(text=stats_texto)
                
        except Exception as e:
            # ✅ CORRECCIÓN N3: Ya no oculta el error
            logging.error(f"Error al actualizar datos: {e}")
            # No mostrar popup para no molestar al usuario durante actualización automática
    
    def abrir_panel_admin(self):
        """Abre panel de administrador con verificacion de contrasena"""
        try:
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
                    usuario_actual = self.logica.usuario_actual.get('usuario') if self.logica.usuario_actual else None
                    
                    if not usuario_actual:
                        messagebox.showerror("Error", "No hay usuario activo")
                        return
                    
                    if self.logica.login(usuario_actual, contrasena):
                        ventana_auth.destroy()
                        self.mostrar_panel_edicion()
                    else:
                        messagebox.showerror("Error", "Contrasena incorrecta")
                        entrada_pass.delete(0, ctk.END)
                        entrada_pass.focus()
                except Exception as e:
                    logging.error(f"Error al verificar: {e}")
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
        except Exception as e:
            logging.error(f"Error al abrir panel admin: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def mostrar_panel_edicion(self):
        """Muestra panel para editar base de datos de productos"""
        try:
            # ✅ CORRECCIÓN: Agregar verificación de administrador
            logging.info(f"Accediendo a panel de edición. Usuario actual: {self.logica.usuario_actual}")
            
            # Verificar que hay un usuario logueado
            if not self.logica.usuario_actual:
                logging.warning("No hay usuario logueado")
                messagebox.showerror("Error de Sesión", 
                    "No hay una sesión activa. Por favor, reinicie la aplicación.")
                return
            
            # Verificar permisos de administrador
            if not self.logica.es_administrador():
                usuario = self.logica.usuario_actual.get('usuario', 'desconocido')
                logging.warning(f"Usuario '{usuario}' sin permisos de admin")
                messagebox.showerror("Acceso Denegado", 
                    "Solo el administrador puede editar productos.\n\n" +
                    "Inicie sesión con la cuenta 'admin' para acceder.")
                return
            
            logging.info("Permisos verificados - Mostrando panel de edición")
            
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
                try:
                    producto_id = UIHelper.extraer_producto_id(combo_productos.get())
                    if not producto_id:
                        logging.warning("No se pudo extraer ID del producto seleccionado")
                        return
                    
                    producto = self.logica.obtener_producto(producto_id)
                    if not producto:
                        logging.error(f"Producto con ID {producto_id} no encontrado")
                        messagebox.showerror("Error", "Producto no encontrado")
                        return
                    
                    # Validar que producto es un diccionario
                    if not isinstance(producto, dict):
                        logging.error(f"Producto retornado no es un diccionario: {type(producto)}")
                        messagebox.showerror("Error", "Error al cargar datos del producto")
                        return
                    
                    entrada_nombre.delete(0, ctk.END)
                    entrada_nombre.insert(0, producto.get('nombre', ''))
                    entrada_precio.delete(0, ctk.END)
                    entrada_precio.insert(0, str(producto.get('precio', '')))
                    entrada_stock.delete(0, ctk.END)
                    entrada_stock.insert(0, str(producto.get('stock', '')))
                    entrada_stock_min.delete(0, ctk.END)
                    entrada_stock_min.insert(0, str(producto.get('stock_minimo', '')))
                    entrada_descripcion.delete("1.0", ctk.END)
                    entrada_descripcion.insert("1.0", producto.get('descripcion') or "")
                    
                    logging.info(f"Producto {producto_id} cargado exitosamente")
                except Exception as e:
                    logging.error(f"Error al cargar producto: {e}", exc_info=True)
                    messagebox.showerror("Error", f"Error al cargar producto:\n{str(e)}")
            
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
                        logging.error(f"Error al actualizar producto: {e}")
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
            
            combo_productos.bind("<<ComboboxSelected>>", lambda e: cargar_producto())
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
                """Actualiza la tabla de productos con validación"""
                try:
                    tabla_admin.delete(*tabla_admin.get_children())
                    productos = self.logica.obtener_productos()
                    
                    if not productos:
                        logging.warning("No hay productos para mostrar en la tabla")
                        return
                    
                    for p in productos:
                        if not isinstance(p, dict):
                            logging.warning(f"Producto inválido encontrado: {p}")
                            continue
                        
                        try:
                            tabla_admin.insert("", "end", values=(
                                p.get('id', ''), 
                                p.get('nombre', ''), 
                                f"${p.get('precio', 0):.2f}", 
                                p.get('stock', 0), 
                                p.get('stock_minimo', 0), 
                                p.get('descripcion', '')[:30]
                            ))
                        except Exception as e:
                            logging.error(f"Error al insertar producto en tabla: {e}")
                            continue
                    
                    logging.info(f"Tabla actualizada con {len(productos)} productos")
                except Exception as e:
                    logging.error(f"Error al actualizar tabla: {e}", exc_info=True)
                    messagebox.showerror("Error", f"Error al actualizar tabla:\n{str(e)}")
            
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
                        logging.error(f"Error al eliminar producto: {e}")
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
        except Exception as e:
            logging.error(f"Error al mostrar panel de edición: {e}")
            messagebox.showerror("Error", f"Error: {str(e)}")


def main():
    """Punto de entrada de la aplicación"""
    ventana_login = VentanaLogin()
    ventana_login.mainloop()


if __name__ == "__main__":
    main()