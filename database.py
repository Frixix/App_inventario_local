"""
CAPA DE DATOS - Gestión de Base de Datos SQLite
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_PATH = "inventario.db"

class DatabaseManager:
    """Clase para gestionar la base de datos SQLite"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
    
    def get_connection(self):
        """Obtiene conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de Usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL,
                nombre TEXT NOT NULL,
                email TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de Productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                precio REAL NOT NULL,
                stock INTEGER DEFAULT 0,
                stock_minimo INTEGER DEFAULT 10,
                descripcion TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de Entradas (Compras/Reposición)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entradas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                proveedor TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_id INTEGER,
                FOREIGN KEY(producto_id) REFERENCES productos(id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Tabla de Salidas (Ventas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS salidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                descuento REAL DEFAULT 0,
                cliente TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                usuario_id INTEGER,
                factura_id INTEGER,
                FOREIGN KEY(producto_id) REFERENCES productos(id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(factura_id) REFERENCES facturas(id)
            )
        ''')
        
        # Tabla de Facturas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cliente_nombre TEXT NOT NULL,
                cliente_nit TEXT,
                cliente_email TEXT,
                cliente_telefono TEXT,
                subtotal REAL DEFAULT 0,
                descuento_total REAL DEFAULT 0,
                iva_porcentaje REAL DEFAULT 19,
                iva_valor REAL DEFAULT 0,
                total REAL DEFAULT 0,
                usuario_id INTEGER,
                notas TEXT,
                estado TEXT DEFAULT 'Activa',
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        ''')
        
        # Verificar si el usuario admin existe, si no crearlo
        cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'")
        if cursor.fetchone() is None:
            cursor.execute('''
                INSERT INTO usuarios (usuario, contraseña, nombre, email)
                VALUES (?, ?, ?, ?)
            ''', ('admin', '1234', 'Administrador', 'admin@inventario.local'))
        
        conn.commit()
        conn.close()
    
    # ==================== USUARIOS ====================
    def verificar_usuario(self, usuario, contraseña):
        """Verifica credenciales de usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, usuario, nombre FROM usuarios WHERE usuario=? AND contraseña=?",
            (usuario, contraseña)
        )
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def crear_usuario(self, usuario, contraseña, nombre, email=None):
        """Crea un nuevo usuario"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (usuario, contraseña, nombre, email)
                VALUES (?, ?, ?, ?)
            ''', (usuario, contraseña, nombre, email))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    # ==================== PRODUCTOS ====================
    def crear_producto(self, nombre, precio, stock=0, stock_minimo=10, descripcion=None):
        """Crea un nuevo producto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO productos (nombre, precio, stock, stock_minimo, descripcion)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, precio, stock, stock_minimo, descripcion))
            conn.commit()
            producto_id = cursor.lastrowid
            conn.close()
            return producto_id
        except sqlite3.IntegrityError:
            return None
    
    def obtener_productos(self):
        """Obtiene todos los productos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY nombre")
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return productos
    
    def obtener_producto(self, producto_id):
        """Obtiene un producto específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id=?", (producto_id,))
        resultado = cursor.fetchone()
        conn.close()
        return dict(resultado) if resultado else None
    
    def actualizar_stock(self, producto_id, cantidad):
        """Actualiza el stock de un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET stock=stock+? WHERE id=?",
            (cantidad, producto_id)
        )
        conn.commit()
        conn.close()
    
    def establecer_stock(self, producto_id, cantidad_nueva):
        """Establece el stock de un producto a un valor específico (modo administrador)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET stock=? WHERE id=?",
            (cantidad_nueva, producto_id)
        )
        conn.commit()
        conn.close()
    
    def obtener_stock(self, producto_id):
        """Obtiene el stock actual de un producto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT stock FROM productos WHERE id=?", (producto_id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado['stock'] if resultado else 0
    
    # ==================== ENTRADAS ====================
    def registrar_entrada(self, producto_id, cantidad, precio_unitario, proveedor=None, usuario_id=None):
        """Registra una entrada de producto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Insertar entrada
            cursor.execute('''
                INSERT INTO entradas (producto_id, cantidad, precio_unitario, proveedor, usuario_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (producto_id, cantidad, precio_unitario, proveedor, usuario_id))
            
            # Actualizar stock
            cursor.execute(
                "UPDATE productos SET stock=stock+? WHERE id=?",
                (cantidad, producto_id)
            )
            
            conn.commit()
            entrada_id = cursor.lastrowid
            conn.close()
            return entrada_id
        except Exception as e:
            print(f"Error al registrar entrada: {e}")
            return None
    
    def obtener_entradas(self):
        """Obtiene todas las entradas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.*, p.nombre FROM entradas e
            JOIN productos p ON e.producto_id = p.id
            ORDER BY e.fecha DESC
        ''')
        entradas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return entradas
    
    # ==================== SALIDAS ====================
    def registrar_salida(self, producto_id, cantidad, precio_unitario, cliente=None, usuario_id=None, factura_id=None):
        """Registra una salida de producto"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Verificar stock disponible
            stock_actual = self.obtener_stock(producto_id)
            if stock_actual < cantidad:
                return None  # Stock insuficiente
            
            # Insertar salida
            cursor.execute('''
                INSERT INTO salidas (producto_id, cantidad, precio_unitario, cliente, usuario_id, factura_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (producto_id, cantidad, precio_unitario, cliente, usuario_id, factura_id))
            
            # Actualizar stock
            cursor.execute(
                "UPDATE productos SET stock=stock-? WHERE id=?",
                (cantidad, producto_id)
            )
            
            conn.commit()
            salida_id = cursor.lastrowid
            conn.close()
            return salida_id
        except Exception as e:
            print(f"Error al registrar salida: {e}")
            return None
    
    def obtener_salidas(self):
        """Obtiene todas las salidas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, p.nombre FROM salidas s
            JOIN productos p ON s.producto_id = p.id
            ORDER BY s.fecha DESC
        ''')
        salidas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return salidas
    
    # ==================== FACTURAS ====================
    def generar_numero_factura(self):
        """Genera un número de factura único"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM facturas")
        count = cursor.fetchone()['count']
        conn.close()
        
        fecha = datetime.now().strftime("%Y%m%d")
        numero = str(count + 1).zfill(6)
        return f"FAC-{fecha}-{numero}"
    
    def crear_factura(self, cliente_nombre, cliente_nit=None, cliente_email=None, 
                     cliente_telefono=None, usuario_id=None, notas=None):
        """Crea una nueva factura"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            numero_factura = self.generar_numero_factura()
            
            cursor.execute('''
                INSERT INTO facturas (numero_factura, cliente_nombre, cliente_nit, 
                                     cliente_email, cliente_telefono, usuario_id, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (numero_factura, cliente_nombre, cliente_nit, cliente_email, 
                  cliente_telefono, usuario_id, notas))
            
            conn.commit()
            factura_id = cursor.lastrowid
            conn.close()
            return factura_id
        except Exception as e:
            print(f"Error al crear factura: {e}")
            return None
    
    def agregar_item_factura(self, factura_id, producto_id, cantidad, usuario_id=None):
        """Agrega un item a la factura y registra salida"""
        try:
            producto = self.obtener_producto(producto_id)
            if not producto:
                return None
            
            # Registrar salida
            salida_id = self.registrar_salida(
                producto_id, cantidad, producto['precio'], 
                usuario_id=usuario_id, factura_id=factura_id
            )
            
            if salida_id:
                return salida_id
            return None
        except Exception as e:
            print(f"Error al agregar item: {e}")
            return None
    
    def actualizar_totales_factura(self, factura_id, iva_porcentaje=19):
        """Calcula y actualiza los totales de la factura"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Obtener suma de salidas
            cursor.execute('''
                SELECT SUM(cantidad * precio_unitario - COALESCE(descuento, 0)) as subtotal
                FROM salidas WHERE factura_id = ?
            ''', (factura_id,))
            
            resultado = cursor.fetchone()
            subtotal = resultado['subtotal'] if resultado['subtotal'] else 0
            
            iva_valor = subtotal * (iva_porcentaje / 100)
            total = subtotal + iva_valor
            
            cursor.execute('''
                UPDATE facturas 
                SET subtotal=?, iva_porcentaje=?, iva_valor=?, total=?
                WHERE id=?
            ''', (subtotal, iva_porcentaje, iva_valor, total, factura_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar totales: {e}")
            return False
    
    def obtener_factura(self, factura_id):
        """Obtiene datos de una factura específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM facturas WHERE id=?", (factura_id,))
        resultado = cursor.fetchone()
        conn.close()
        return dict(resultado) if resultado else None
    
    def obtener_items_factura(self, factura_id):
        """Obtiene los items de una factura"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.*, p.nombre FROM salidas s
            JOIN productos p ON s.producto_id = p.id
            WHERE s.factura_id = ?
            ORDER BY s.id
        ''', (factura_id,))
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items
    
    def obtener_facturas(self):
        """Obtiene todas las facturas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM facturas ORDER BY fecha DESC")
        facturas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return facturas
