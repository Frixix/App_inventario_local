"""
CAPA DE INTERFAZ - GUI con tkinter
Aplicación de Escritorio para Inventario
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from logica import LogicaInventario
from facturas import GeneradorFactura

class VentanaLogin(tk.Tk):
    """Ventana de login"""
    
    def __init__(self):
        super().__init__()
        self.title("Inventario - Login")
        self.geometry("400x280")
        self.resizable(False, False)
        
        try:
            self.logica = LogicaInventario()
            self.crearUI()
        except Exception as e:
            messagebox.showerror("Error de Inicialización", 
                                f"Error al cargar la aplicación:\n{str(e)}")
            self.destroy()
    
    def crearUI(self):
        """Crea interfaz de login"""
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(frame, text="Sistema de Inventario", 
                          font=("Arial", 16, "bold"))
        titulo.pack(pady=10)
        
        subtitulo = ttk.Label(frame, text="Ingrese sus credenciales",
                             font=("Arial", 10))
        subtitulo.pack(pady=5)
        
        # Usuario
        ttk.Label(frame, text="Usuario:").pack(anchor=tk.W, pady=(10, 0))
        self.entrada_usuario = ttk.Entry(frame, width=30)
        self.entrada_usuario.pack(fill=tk.X, pady=(0, 10))
        
        # Contraseña
        ttk.Label(frame, text="Contraseña:").pack(anchor=tk.W)
        self.entrada_contraseña = ttk.Entry(frame, width=30, show="*")
        self.entrada_contraseña.pack(fill=tk.X, pady=(0, 30))
        
        # Botón principal - Ingresar (grande y prominente)
        btn_login = tk.Button(frame, text="▶ INGRESAR", 
                             command=self.hacer_login,
                             bg="#4CAF50", fg="white",
                             font=("Arial", 12, "bold"),
                             padx=20, pady=10,
                             cursor="hand2")
        btn_login.pack(fill=tk.X, pady=10)
        
        # Botones secundarios
        frame_botones = ttk.Frame(frame)
        frame_botones.pack(fill=tk.X, pady=10)
        
        btn_salir = ttk.Button(frame_botones, text="Salir",
                               command=self.salir_app)
        btn_salir.pack(side=tk.RIGHT, padx=5)
        
        # Hint para usuario
        hint = ttk.Label(frame, text="Prueba: admin / 1234", 
                        font=("Arial", 8), foreground="gray")
        hint.pack(pady=(5, 0))
        
        self.entrada_usuario.focus()
        
        # Permitir Enter en campos de entrada
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
                self.entrada_contraseña.delete(0, tk.END)
                self.entrada_usuario.focus()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión:\n{str(e)}")
    
    def salir_app(self):
        """Cierra la aplicación correctamente"""
        if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
            self.destroy()
            self.entrada_contraseña.delete(0, tk.END)


class AplicacionInventario(tk.Tk):
    """Aplicación principal de inventario"""
    
    def __init__(self, logica):
        super().__init__()
        self.title("Sistema de Inventario Local")
        self.geometry("900x700")
        self.logica = logica
        self.generador_facturas = GeneradorFactura(logica)
        self.factura_actual = None
        
        # Estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.crearUI()
        self.actualizar_datos()
    
    def crearUI(self):
        """Crea interfaz principal"""
        # Barra de menú
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Salir", command=self.salir)
        
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca)
        
        # Barra superior con información
        frame_superior = ttk.Frame(self)
        frame_superior.pack(fill=tk.X, padx=10, pady=10)
        
        usuario = self.logica.get_usuario_actual()
        ttk.Label(frame_superior, text=f"Bienvenido: {usuario['nombre']}", 
                 font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        ttk.Label(frame_superior, text=f"Hora: {datetime.now().strftime('%H:%M:%S')}", 
                 font=("Arial", 9)).pack(side=tk.RIGHT)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña 1: Productos
        self.crear_pestaña_productos()
        
        # Pestaña 2: Entradas
        self.crear_pestaña_entradas()
        
        # Pestaña 3: Salidas
        self.crear_pestaña_salidas()
        
        # Pestaña 4: Facturas
        self.crear_pestaña_facturas()
        
        # Pestaña 5: Reportes
        self.crear_pestaña_reportes()
    
    def crear_pestaña_productos(self):
        """Crea pestaña de gestión de productos"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📦 Productos")
        
        # Panel de entrada
        frame_entrada = ttk.LabelFrame(frame, text="Crear Nuevo Producto", padding="10")
        frame_entrada.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_entrada, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entrada_nombre = ttk.Entry(frame_entrada, width=30)
        self.entrada_nombre.grid(row=0, column=1, padx=10)
        
        ttk.Label(frame_entrada, text="Precio:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrada_precio = ttk.Entry(frame_entrada, width=15)
        self.entrada_precio.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(frame_entrada, text="Stock:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrada_stock = ttk.Entry(frame_entrada, width=15)
        self.entrada_stock.grid(row=2, column=1, sticky=tk.W, padx=10)
        self.entrada_stock.insert(0, "0")
        
        ttk.Label(frame_entrada, text="Stock Mínimo:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entrada_stock_min = ttk.Entry(frame_entrada, width=15)
        self.entrada_stock_min.grid(row=3, column=1, sticky=tk.W, padx=10)
        self.entrada_stock_min.insert(0, "10")
        
        ttk.Button(frame_entrada, text="Crear Producto",
                  command=self.crear_producto).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Lista de productos
        frame_lista = ttk.LabelFrame(frame, text="Lista de Productos", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabla
        columnas = ("ID", "Nombre", "Precio", "Stock", "Mínimo", "Estado")
        self.tabla_productos = ttk.Treeview(frame_lista, columns=columnas, height=12)
        
        self.tabla_productos.column("#0", width=0, stretch=tk.NO)
        self.tabla_productos.column("ID", anchor=tk.CENTER, width=40)
        self.tabla_productos.column("Nombre", anchor=tk.W, width=200)
        self.tabla_productos.column("Precio", anchor=tk.CENTER, width=80)
        self.tabla_productos.column("Stock", anchor=tk.CENTER, width=80)
        self.tabla_productos.column("Mínimo", anchor=tk.CENTER, width=80)
        self.tabla_productos.column("Estado", anchor=tk.CENTER, width=120)
        
        self.tabla_productos.heading("#0", text="", anchor=tk.W)
        self.tabla_productos.heading("ID", text="ID", anchor=tk.CENTER)
        self.tabla_productos.heading("Nombre", text="Nombre", anchor=tk.W)
        self.tabla_productos.heading("Precio", text="Precio", anchor=tk.CENTER)
        self.tabla_productos.heading("Stock", text="Stock", anchor=tk.CENTER)
        self.tabla_productos.heading("Mínimo", text="Mínimo", anchor=tk.CENTER)
        self.tabla_productos.heading("Estado", text="Estado", anchor=tk.CENTER)
        
        self.tabla_productos.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestaña_entradas(self):
        """Crea pestaña de entradas (compras)"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📥 Entradas")
        
        # Panel de entrada
        frame_entrada = ttk.LabelFrame(frame, text="Registrar Entrada", padding="10")
        frame_entrada.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_entrada, text="Producto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_producto_entrada = ttk.Combobox(frame_entrada, width=30, state="readonly")
        self.combo_producto_entrada.grid(row=0, column=1, padx=10)
        
        ttk.Label(frame_entrada, text="Cantidad:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrada_cantidad_entrada = ttk.Entry(frame_entrada, width=15)
        self.entrada_cantidad_entrada.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(frame_entrada, text="Precio Unitario:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrada_precio_entrada = ttk.Entry(frame_entrada, width=15)
        self.entrada_precio_entrada.grid(row=2, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(frame_entrada, text="Proveedor:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entrada_proveedor = ttk.Entry(frame_entrada, width=30)
        self.entrada_proveedor.grid(row=3, column=1, padx=10)
        
        ttk.Button(frame_entrada, text="Registrar Entrada",
                  command=self.registrar_entrada).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Lista de entradas
        frame_lista = ttk.LabelFrame(frame, text="Historial de Entradas", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columnas = ("ID", "Producto", "Cantidad", "Precio", "Proveedor", "Fecha")
        self.tabla_entradas = ttk.Treeview(frame_lista, columns=columnas, height=10)
        
        self.tabla_entradas.column("#0", width=0, stretch=tk.NO)
        self.tabla_entradas.column("ID", anchor=tk.CENTER, width=40)
        self.tabla_entradas.column("Producto", anchor=tk.W, width=200)
        self.tabla_entradas.column("Cantidad", anchor=tk.CENTER, width=80)
        self.tabla_entradas.column("Precio", anchor=tk.CENTER, width=80)
        self.tabla_entradas.column("Proveedor", anchor=tk.W, width=150)
        self.tabla_entradas.column("Fecha", anchor=tk.CENTER, width=120)
        
        for col in columnas:
            self.tabla_entradas.heading(col, text=col)
        
        self.tabla_entradas.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestaña_salidas(self):
        """Crea pestaña de salidas (ventas)"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📤 Salidas")
        
        # Panel de entrada
        frame_entrada = ttk.LabelFrame(frame, text="Registrar Salida", padding="10")
        frame_entrada.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_entrada, text="Producto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_producto_salida = ttk.Combobox(frame_entrada, width=30, state="readonly")
        self.combo_producto_salida.grid(row=0, column=1, padx=10)
        
        ttk.Label(frame_entrada, text="Cantidad:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrada_cantidad_salida = ttk.Entry(frame_entrada, width=15)
        self.entrada_cantidad_salida.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(frame_entrada, text="Cliente:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrada_cliente = ttk.Entry(frame_entrada, width=30)
        self.entrada_cliente.grid(row=2, column=1, padx=10)
        
        btn_frame = ttk.Frame(frame_entrada)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Salida Sin Factura",
                  command=self.registrar_salida).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Crear Factura",
                  command=self.crear_factura_desde_salida).pack(side=tk.LEFT, padx=5)
        
        # Lista de salidas
        frame_lista = ttk.LabelFrame(frame, text="Historial de Salidas", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columnas = ("ID", "Producto", "Cantidad", "Cliente", "Fecha")
        self.tabla_salidas = ttk.Treeview(frame_lista, columns=columnas, height=10)
        
        self.tabla_salidas.column("#0", width=0, stretch=tk.NO)
        self.tabla_salidas.column("ID", anchor=tk.CENTER, width=40)
        self.tabla_salidas.column("Producto", anchor=tk.W, width=200)
        self.tabla_salidas.column("Cantidad", anchor=tk.CENTER, width=80)
        self.tabla_salidas.column("Cliente", anchor=tk.W, width=200)
        self.tabla_salidas.column("Fecha", anchor=tk.CENTER, width=120)
        
        for col in columnas:
            self.tabla_salidas.heading(col, text=col)
        
        self.tabla_salidas.pack(fill=tk.BOTH, expand=True)
    
    def crear_pestaña_facturas(self):
        """Crea pestaña de gestión de facturas"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🧾 Facturas")
        
        # Panel de control
        frame_control = ttk.LabelFrame(frame, text="Nueva Factura", padding="10")
        frame_control.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_control, text="Cliente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entrada_factura_cliente = ttk.Entry(frame_control, width=30)
        self.entrada_factura_cliente.grid(row=0, column=1, padx=10)
        
        ttk.Label(frame_control, text="NIT:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrada_factura_nit = ttk.Entry(frame_control, width=30)
        self.entrada_factura_nit.grid(row=1, column=1, padx=10)
        
        ttk.Label(frame_control, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrada_factura_email = ttk.Entry(frame_control, width=30)
        self.entrada_factura_email.grid(row=2, column=1, padx=10)
        
        ttk.Label(frame_control, text="Teléfono:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entrada_factura_telefono = ttk.Entry(frame_control, width=30)
        self.entrada_factura_telefono.grid(row=3, column=1, padx=10)
        
        ttk.Button(frame_control, text="Nueva Factura",
                  command=self.nueva_factura).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Panel de edición de factura
        frame_edicion = ttk.LabelFrame(frame, text="Agregar Productos a Factura", padding="10")
        frame_edicion.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_edicion, text="Producto:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_producto_factura = ttk.Combobox(frame_edicion, width=30, state="readonly")
        self.combo_producto_factura.grid(row=0, column=1, padx=10)
        
        ttk.Label(frame_edicion, text="Cantidad:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrada_cantidad_factura = ttk.Entry(frame_edicion, width=15)
        self.entrada_cantidad_factura.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        btn_frame = ttk.Frame(frame_edicion)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Agregar a Factura",
                  command=self.agregar_producto_factura).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Ver Factura",
                  command=self.ver_factura_actual).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Finalizar Factura",
                  command=self.finalizar_factura).pack(side=tk.LEFT, padx=5)
        
        # Lista de facturas
        frame_lista = ttk.LabelFrame(frame, text="Listado de Facturas", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columnas = ("Número", "Cliente", "Fecha", "Total", "Estado")
        self.tabla_facturas = ttk.Treeview(frame_lista, columns=columnas, height=8)
        
        self.tabla_facturas.column("#0", width=0, stretch=tk.NO)
        for col in columnas:
            self.tabla_facturas.column(col, anchor=tk.CENTER, width=120)
            self.tabla_facturas.heading(col, text=col)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tabla_facturas.yview)
        self.tabla_facturas.configure(yscroll=scrollbar.set)
        
        self.tabla_facturas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Eventos
        self.tabla_facturas.bind("<Double-1>", self.ver_factura_seleccionada)
    
    def crear_pestaña_reportes(self):
        """Crea pestaña de reportes"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Reportes")
        
        # Estadísticas
        frame_stats = ttk.LabelFrame(frame, text="Estadísticas General", padding="10")
        frame_stats.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_stats = ttk.Label(frame_stats, text="", font=("Arial", 10))
        self.label_stats.pack(fill=tk.X)
        
        # Productos bajo stock
        frame_alerta = ttk.LabelFrame(frame, text="Productos Bajo Stock", padding="10")
        frame_alerta.pack(fill=tk.X, padx=10, pady=10)
        
        columnas = ("ID", "Nombre", "Stock", "Mínimo")
        self.tabla_bajo_stock = ttk.Treeview(frame_alerta, columns=columnas, height=6)
        
        self.tabla_bajo_stock.column("#0", width=0, stretch=tk.NO)
        for col in columnas:
            self.tabla_bajo_stock.column(col, anchor=tk.CENTER, width=120)
            self.tabla_bajo_stock.heading(col, text=col)
        
        self.tabla_bajo_stock.pack(fill=tk.X)
        
        # Botones de acción
        frame_botones = ttk.Frame(frame)
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_botones, text="Actualizar",
                  command=self.actualizar_datos).pack(side=tk.LEFT, padx=5)
    
    # ==================== MÉTODOS DE PRODUCTOS ====================
    def crear_producto(self):
        """Crea un nuevo producto"""
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
                messagebox.showinfo("Éxito", "Producto creado correctamente")
                self.entrada_nombre.delete(0, tk.END)
                self.entrada_precio.delete(0, tk.END)
                self.entrada_stock.delete(0, tk.END)
                self.entrada_stock.insert(0, "0")
                self.entrada_stock_min.delete(0, tk.END)
                self.entrada_stock_min.insert(0, "10")
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo crear el producto")
        except ValueError:
            messagebox.showerror("Error", "Precio y stock deben ser números")
    
    # ==================== MÉTODOS DE ENTRADAS ====================
    def registrar_entrada(self):
        """Registra una entrada de producto"""
        producto_id_str = self.combo_producto_entrada.get()
        cantidad_str = self.entrada_cantidad_entrada.get().strip()
        precio_str = self.entrada_precio_entrada.get().strip()
        proveedor = self.entrada_proveedor.get().strip()
        
        if not producto_id_str or not cantidad_str or not precio_str:
            messagebox.showerror("Error", "Complete todos los campos requeridos")
            return
        
        try:
            # Extraer ID del string "ID - Nombre"
            producto_id = int(producto_id_str.split(" ")[0])
            cantidad = int(cantidad_str)
            precio = float(precio_str)
            
            if self.logica.registrar_entrada(producto_id, cantidad, precio, proveedor):
                messagebox.showinfo("Éxito", "Entrada registrada correctamente")
                self.entrada_cantidad_entrada.delete(0, tk.END)
                self.entrada_precio_entrada.delete(0, tk.END)
                self.entrada_proveedor.delete(0, tk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo registrar la entrada")
        except ValueError:
            messagebox.showerror("Error", "Verifique cantidad y precio")
    
    # ==================== MÉTODOS DE SALIDAS ====================
    def registrar_salida(self):
        """Registra una salida de producto"""
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
                messagebox.showinfo("Éxito", "Salida registrada correctamente")
                self.entrada_cantidad_salida.delete(0, tk.END)
                self.entrada_cliente.delete(0, tk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "Stock insuficiente o error en salida")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número")
    
    # ==================== MÉTODOS DE FACTURAS ====================
    def nueva_factura(self):
        """Crea una nueva factura"""
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
            messagebox.showinfo("Éxito", f"Factura creada: {factura_id}")
            self.entrada_cantidad_factura.delete(0, tk.END)
            self.entrada_cantidad_factura.focus()
        else:
            messagebox.showerror("Error", "No se pudo crear factura")
    
    def crear_factura_desde_salida(self):
        """Crea una factura desde salida"""
        producto_id_str = self.combo_producto_salida.get()
        cantidad_str = self.entrada_cantidad_salida.get().strip()
        cliente = self.entrada_cliente.get().strip()
        
        if not producto_id_str or not cantidad_str or not cliente:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        try:
            producto_id = int(producto_id_str.split(" ")[0])
            cantidad = int(cantidad_str)
            
            # Crear factura
            factura_id = self.logica.crear_nueva_factura(cliente)
            if not factura_id:
                messagebox.showerror("Error", "No se pudo crear factura")
                return
            
            # Agregar producto
            if self.logica.agregar_producto_factura(factura_id, producto_id, cantidad):
                self.factura_actual = factura_id
                messagebox.showinfo("Éxito", "Factura creada con producto")
                self.entrada_cantidad_salida.delete(0, tk.END)
                self.entrada_cliente.delete(0, tk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo agregar producto a factura")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número")
    
    def agregar_producto_factura(self):
        """Agrega producto a factura actual"""
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
                messagebox.showinfo("Éxito", "Producto agregado a factura")
                self.entrada_cantidad_factura.delete(0, tk.END)
                self.actualizar_datos()
            else:
                messagebox.showerror("Error", "No se pudo agregar producto")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número")
    
    def ver_factura_actual(self):
        """Visualiza la factura actual"""
        if not self.factura_actual:
            messagebox.showerror("Error", "No hay factura abierta")
            return
        
        self.mostrar_ventana_factura(self.factura_actual)
    
    def ver_factura_seleccionada(self, event):
        """Visualiza factura seleccionada en tabla"""
        seleccion = self.tabla_facturas.selection()
        if not seleccion:
            return
        
        item = seleccion[0]
        numero_factura = self.tabla_facturas.item(item)['values'][0]
        
        # Buscar ID de factura por número
        facturas = self.logica.obtener_facturas()
        for f in facturas:
            if f['numero_factura'] == numero_factura:
                self.mostrar_ventana_factura(f['id'])
                break
    
    def mostrar_ventana_factura(self, factura_id):
        """Abre ventana para visualizar factura"""
        texto_factura = self.generador_facturas.generar_texto_factura(factura_id)
        
        if not texto_factura:
            messagebox.showerror("Error", "No se pudo generar factura")
            return
        
        ventana = tk.Toplevel(self)
        ventana.title("Vista de Factura")
        ventana.geometry("600x700")
        
        texto_widget = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, font=("Courier", 9))
        texto_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        texto_widget.insert(tk.END, texto_factura)
        texto_widget.config(state=tk.DISABLED)
        
        frame_botones = ttk.Frame(ventana)
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        factura = self.logica.obtener_factura(factura_id)
        
        ttk.Button(frame_botones, text="Guardar como TXT",
                  command=lambda: self.guardar_factura_txt(factura_id)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="Guardar como HTML",
                  command=lambda: self.guardar_factura_html(factura_id)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="Cerrar", command=ventana.destroy).pack(side=tk.RIGHT, padx=5)
    
    def guardar_factura_txt(self, factura_id):
        """Guarda factura como TXT"""
        if self.generador_facturas.guardar_factura_txt(factura_id):
            messagebox.showinfo("Éxito", "Factura guardada en Facturas/")
        else:
            messagebox.showerror("Error", "No se pudo guardar factura")
    
    def guardar_factura_html(self, factura_id):
        """Guarda factura como HTML"""
        if self.generador_facturas.guardar_factura_html(factura_id):
            messagebox.showinfo("Éxito", "Factura guardada en Facturas/")
        else:
            messagebox.showerror("Error", "No se pudo guardar factura")
    
    def finalizar_factura(self):
        """Finaliza factura actual"""
        if not self.factura_actual:
            messagebox.showerror("Error", "No hay factura abierta")
            return
        
        self.mostrar_ventana_factura(self.factura_actual)
        self.factura_actual = None
        messagebox.showinfo("Éxito", "Factura finalizada")
        self.actualizar_datos()
    
    # ==================== ACTUALIZACIÓN DE DATOS ====================
    def actualizar_datos(self):
        """Actualiza todas las tablas y listas"""
        # Actualizar lista de productos
        self.tabla_productos.delete(*self.tabla_productos.get_children())
        productos = self.logica.obtener_productos()
        
        for p in productos:
            estado = "✓ OK" if p['stock'] >= p['stock_minimo'] else "⚠ BAJO"
            self.tabla_productos.insert("", tk.END, values=(
                p['id'], p['nombre'], f"${p['precio']:.2f}", 
                p['stock'], p['stock_minimo'], estado
            ))
        
        # Actualizar combos
        combo_items = [f"{p['id']} - {p['nombre']}" for p in productos]
        self.combo_producto_entrada.config(values=combo_items)
        self.combo_producto_salida.config(values=combo_items)
        self.combo_producto_factura.config(values=combo_items)
        
        # Actualizar entradas
        self.tabla_entradas.delete(*self.tabla_entradas.get_children())
        entradas = self.logica.obtener_entradas()
        for e in entradas[:10]:  # Últimas 10
            self.tabla_entradas.insert("", tk.END, values=(
                e['id'], e['nombre'], e['cantidad'],
                f"${e['precio_unitario']:.2f}", e['proveedor'] or "-", e['fecha'][:10]
            ))
        
        # Actualizar salidas
        self.tabla_salidas.delete(*self.tabla_salidas.get_children())
        salidas = self.logica.obtener_salidas()
        for s in salidas[:10]:  # Últimas 10
            self.tabla_salidas.insert("", tk.END, values=(
                s['id'], s['nombre'], s['cantidad'], 
                s['cliente'] or "-", s['fecha'][:10]
            ))
        
        # Actualizar facturas
        self.tabla_facturas.delete(*self.tabla_facturas.get_children())
        facturas = self.logica.obtener_facturas()
        for f in facturas:
            self.tabla_facturas.insert("", tk.END, values=(
                f['numero_factura'], f['cliente_nombre'],
                f['fecha'][:10], f"${f['total']:.2f}", f['estado']
            ))
        
        # Actualizar productos bajo stock
        self.tabla_bajo_stock.delete(*self.tabla_bajo_stock.get_children())
        bajo_stock = self.logica.productos_bajo_stock()
        for p in bajo_stock:
            self.tabla_bajo_stock.insert("", tk.END, values=(
                p['id'], p['nombre'], p['stock'], p['stock_minimo']
            ))
        
        # Actualizar estadísticas
        stats = self.logica.obtener_estadisticas()
        stats_texto = f"""
Productos: {stats['total_productos']} | Entradas: {stats['total_entradas']} | 
Salidas: {stats['total_salidas']} | Facturas: {stats['total_facturas']} |
Bajo Stock: {stats['productos_bajo_stock']} | Valor Inventario: ${stats['valor_inventario']:.2f}
        """
        self.label_stats.config(text=stats_texto.strip())
    
    def salir(self):
        """Cierra la aplicación"""
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.destroy()
    
    def mostrar_acerca(self):
        """Muestra diálogo de información"""
        messagebox.showinfo("Acerca de",
            "Sistema de Inventario Local v1.0\n\n"
            "Aplicación de escritorio para gestión de inventario,\n"
            "entradas, salidas y generación de facturas.\n\n"
            "Base de datos: SQLite")


def main():
    """Función principal"""
    ventana_login = VentanaLogin()
    ventana_login.mainloop()


if __name__ == "__main__":
    main()
