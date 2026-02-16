"""
CAPA DE LOGICA - Gestion de Inventario y Negocio (Optimizada)
"""

from database import DatabaseManager
from datetime import datetime

class LogicaInventario:
    """Clase con la logica de negocio del inventario"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.usuario_actual = None
    
    # ==================== VALIDACIONES ====================
    @staticmethod
    def _validar_cantidad(cantidad):
        """Valida que cantidad sea positiva"""
        return cantidad and cantidad > 0
    
    @staticmethod
    def _validar_precio(precio):
        """Valida que precio sea valido"""
        # ✅ CORREGIDO: Cambiado 'price' por 'precio'
        return precio >= 0 if precio is not None else False
    
    # ==================== AUTENTICACION ====================
    def login(self, usuario, contrasena):
        """Autentica un usuario"""
        resultado = self.db.verificar_usuario(usuario, contrasena)
        if resultado:
            self.usuario_actual = resultado
            return True
        return False
    
    def logout(self):
        """Cierra sesion"""
        self.usuario_actual = None
    
    def get_usuario_actual(self):
        """Obtiene datos del usuario actual"""
        return self.usuario_actual
    
    def es_administrador(self):
        """Verifica si el usuario actual es administrador"""
        if not self.usuario_actual:
            return False
        return self.usuario_actual.get('nombre') == 'Administrador'
    
    # ==================== PRODUCTOS ====================
    def crear_producto(self, nombre, precio, stock=0, stock_minimo=10, descripcion=None):
        """Crea un nuevo producto"""
        # ✅ MEJORADO: Ahora usa la validación de precio
        if not nombre or not self._validar_precio(precio):
            return False
        
        producto_id = self.db.crear_producto(nombre, precio, stock, stock_minimo, descripcion)
        return producto_id is not None
    
    def obtener_productos(self):
        """Obtiene lista de productos"""
        return self.db.obtener_productos()
    
    def obtener_producto(self, producto_id):
        """Obtiene datos de un producto"""
        return self.db.obtener_producto(producto_id)
    
    def obtener_producto_por_nombre(self, nombre):
        """Busca un producto por nombre"""
        productos = self.db.obtener_productos()
        for p in productos:
            if p['nombre'].lower() == nombre.lower():
                return p
        return None
    
    def obtener_stock(self, producto_id):
        """Obtiene stock actual de un producto"""
        return self.db.obtener_stock(producto_id)
    
    def productos_bajo_stock(self):
        """Retorna productos con stock por debajo del minimo"""
        productos = self.db.obtener_productos()
        return [p for p in productos if p['stock'] < p['stock_minimo']]
    
    def cambiar_stock_manual(self, producto_id, cantidad_nueva):
        """Cambia el stock manualmente (solo administrador)"""
        if not self.es_administrador() or cantidad_nueva < 0:
            return False
        
        try:
            self.db.establecer_stock(producto_id, cantidad_nueva)
            return True
        except Exception:
            return False
    
    def _modificar_stock_admin(self, producto_id, cantidad, operacion):
        """Modifica stock - abstraccion comun"""
        if not self.es_administrador() or not self._validar_cantidad(cantidad):
            return False
        
        if operacion == "quitar":
            stock_actual = self.db.obtener_stock(producto_id)
            if stock_actual < cantidad:
                return False
            cantidad = -cantidad
        
        try:
            self.db.actualizar_stock(producto_id, cantidad)
            return True
        except Exception:
            return False
    
    def agregar_stock_manual(self, producto_id, cantidad):
        """Agrega cantidad al stock manualmente (solo administrador)"""
        return self._modificar_stock_admin(producto_id, cantidad, "agregar")
    
    def quitar_stock_manual(self, producto_id, cantidad):
        """Quita cantidad del stock manualmente (solo administrador)"""
        return self._modificar_stock_admin(producto_id, cantidad, "quitar")
    
    # ==================== ENTRADAS ====================
    def registrar_entrada(self, producto_id, cantidad, precio_unitario, proveedor=None):
        """Registra una entrada de producto"""
        # ✅ MEJORADO: Ahora usa la validación de precio
        if not self._validar_cantidad(cantidad) or not self._validar_precio(precio_unitario):
            return False
        
        usuario_id = self.usuario_actual['id'] if self.usuario_actual else None
        entrada_id = self.db.registrar_entrada(
            producto_id, cantidad, precio_unitario, proveedor, usuario_id
        )
        return entrada_id is not None
    
    def obtener_entradas(self):
        """Obtiene historial de entradas"""
        return self.db.obtener_entradas()
    
    def obtener_entradas_producto(self, producto_id):
        """Obtiene entradas de un producto especifico"""
        entradas = self.db.obtener_entradas()
        return [e for e in entradas if e['producto_id'] == producto_id]
    
    # ==================== SALIDAS ====================
    def registrar_salida(self, producto_id, cantidad, cliente=None):
        """Registra una salida de producto"""
        if not self._validar_cantidad(cantidad):
            return False
        
        producto = self.db.obtener_producto(producto_id)
        if not producto:
            return False
        
        usuario_id = self.usuario_actual['id'] if self.usuario_actual else None
        salida_id = self.db.registrar_salida(
            producto_id, cantidad, producto['precio'], cliente, usuario_id
        )
        
        return salida_id is not None
    
    def obtener_salidas(self):
        """Obtiene historial de salidas"""
        return self.db.obtener_salidas()
    
    def obtener_salidas_producto(self, producto_id):
        """Obtiene salidas de un producto especifico"""
        salidas = self.db.obtener_salidas()
        return [s for s in salidas if s['producto_id'] == producto_id]
    
    # ==================== FACTURAS ====================
    def crear_nueva_factura(self, cliente_nombre, cliente_nit=None, cliente_email=None, 
                           cliente_telefono=None, notas=None):
        """Crea una nueva factura"""
        if not cliente_nombre:
            return None
        
        usuario_id = self.usuario_actual['id'] if self.usuario_actual else None
        factura_id = self.db.crear_factura(
            cliente_nombre, cliente_nit, cliente_email, 
            cliente_telefono, usuario_id, notas
        )
        return factura_id
    
    def agregar_producto_factura(self, factura_id, producto_id, cantidad):
        """Agrega un producto a la factura"""
        if not self._validar_cantidad(cantidad):
            return False
        
        producto = self.db.obtener_producto(producto_id)
        if not producto or producto['stock'] < cantidad:
            return False
        
        usuario_id = self.usuario_actual['id'] if self.usuario_actual else None
        item_id = self.db.agregar_item_factura(factura_id, producto_id, cantidad, usuario_id)
        
        if item_id:
            self.db.actualizar_totales_factura(factura_id)
            return True
        
        return False
    
    def obtener_factura(self, factura_id):
        """Obtiene datos de una factura"""
        return self.db.obtener_factura(factura_id)
    
    def obtener_items_factura(self, factura_id):
        """Obtiene items de una factura"""
        return self.db.obtener_items_factura(factura_id)
    
    def obtener_facturas(self):
        """Obtiene todas las facturas"""
        return self.db.obtener_facturas()
    
    def generar_resumen_factura(self, factura_id):
        """Genera un resumen de la factura con formato"""
        factura = self.db.obtener_factura(factura_id)
        items = self.db.obtener_items_factura(factura_id)
        
        if not factura:
            return None
        
        return {
            'numero': factura['numero_factura'],
            'fecha': factura['fecha'],
            'cliente': {
                'nombre': factura['cliente_nombre'],
                'nit': factura['cliente_nit'],
                'email': factura['cliente_email'],
                'telefono': factura['cliente_telefono']
            },
            'items': items,
            'subtotal': factura['subtotal'],
            'iva_porcentaje': factura['iva_porcentaje'],
            'iva_valor': factura['iva_valor'],
            'total': factura['total']
        }
    
    # ==================== REPORTES ====================
    def reporte_movimientos_producto(self, producto_id):
        """Genera reporte de movimientos de un producto"""
        producto = self.db.obtener_producto(producto_id)
        if not producto:
            return None
        
        entradas = self.obtener_entradas_producto(producto_id)
        salidas = self.obtener_salidas_producto(producto_id)
        
        return {
            'producto': producto,
            'entradas': entradas,
            'salidas': salidas,
            'total_entrada': sum(e['cantidad'] for e in entradas),
            'total_salida': sum(s['cantidad'] for s in salidas),
            'stock_actual': producto['stock']
        }
    
    def obtener_estadisticas(self):
        """Obtiene estadisticas generales del inventario"""
        productos = self.db.obtener_productos()
        entradas = self.db.obtener_entradas()
        salidas = self.db.obtener_salidas()
        facturas = self.db.obtener_facturas()
        
        return {
            'total_productos': len(productos),
            'total_entradas': len(entradas),
            'total_salidas': len(salidas),
            'total_facturas': len(facturas),
            'productos_bajo_stock': len(self.productos_bajo_stock()),
            'valor_inventario': sum(p['stock'] * p['precio'] for p in productos),
            'facturas_pendientes': len([f for f in facturas if f['estado'] == 'Activa'])
        }