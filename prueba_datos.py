# 🧪 Script de Prueba - Datos de Ejemplo

"""
Ejecutar este script para cargar datos de prueba en la aplicación
"""

from database import DatabaseManager
from logica import LogicaInventario

def cargar_datos_prueba():
    """Carga datos de ejemplo para probar la aplicación"""
    
    logica = LogicaInventario()
    db = logica.db
    
    print("🔄 Cargando datos de prueba...")
    
    # ==================== PRODUCTOS ====================
    print("\n📦 Creando productos...")
    
    productos = [
        ("Laptop Dell", 1500000, 5, 2, "Laptop para desarrollo"),
        ("Mouse Logitech", 45000, 20, 5, "Mouse inalámbrico"),
        ("Teclado Mecánico", 250000, 10, 3, "Teclado RGB"),
        ("Monitor 24\"", 600000, 8, 2, "Monitor Full HD"),
        ("Escritorio", 800000, 3, 1, "Escritorio de madera"),
        ("Silla Gamer", 450000, 6, 2, "Silla con soporte lumbar"),
        ("Webcam HD", 120000, 15, 5, "Webcam 1080p"),
        ("Micrófono USB", 180000, 12, 4, "Micrófono condensador"),
        ("Cable HDMI", 35000, 50, 10, "Cable HDMI 2m"),
        ("Adaptador USB-C", 55000, 30, 8, "Adaptador USB tipo C"),
    ]
    
    producto_ids = []
    for nombre, precio, stock, stock_min, desc in productos:
        producto_id = logica.crear_producto(nombre, precio, stock, stock_min, desc)
        if producto_id:
            producto_ids.append((producto_id, nombre))
            print(f"  ✓ {nombre}")
    
    # ==================== ENTRADAS ====================
    print("\n📥 Registrando entradas...")
    
    entradas = [
        (producto_ids[0][0], 3, 1300000, "Proveedor Tech Ltda"),
        (producto_ids[1][0], 10, 40000, "Distribuidor Mouse"),
        (producto_ids[2][0], 5, 230000, "Teclados Premium"),
        (producto_ids[3][0], 4, 550000, "Monitores Plus"),
        (producto_ids[4][0], 2, 750000, "Muebles Oferta"),
    ]
    
    for prod_id, cantidad, precio, proveedor in entradas:
        logica.registrar_entrada(prod_id, cantidad, precio, proveedor)
        print(f"  ✓ Entrada registrada")
    
    # ==================== SALIDAS (sin factura) ====================
    print("\n📤 Registrando salidas...")
    
    salidas = [
        (producto_ids[1][0], 2, "Cliente 1"),
        (producto_ids[6][0], 3, "Cliente 2"),
        (producto_ids[7][0], 2, "Cliente 3"),
        (producto_ids[8][0], 5, "Cliente 4"),
    ]
    
    for prod_id, cantidad, cliente in salidas:
        logica.registrar_salida(prod_id, cantidad, cliente)
        print(f"  ✓ Salida registrada")
    
    # ==================== FACTURAS ====================
    print("\n🧾 Generando facturas...")
    
    # Factura 1
    factura_id = logica.crear_nueva_factura(
        "Empresa ABC SAS",
        nit="9876543210",
        email="contacto@abc.com",
        telefono="6015551234"
    )
    
    if factura_id:
        logica.agregar_producto_factura(factura_id, producto_ids[0][0], 1)  # 1 Laptop
        logica.agregar_producto_factura(factura_id, producto_ids[3][0], 1)  # 1 Monitor
        logica.agregar_producto_factura(factura_id, producto_ids[5][0], 1)  # 1 Silla
        print(f"  ✓ Factura 1 creada (3 items)")
    
    # Factura 2
    factura_id2 = logica.crear_nueva_factura(
        "Tienda XYZ",
        nit="1122334455",
        email="ventas@xyz.com",
        telefono="6015559999"
    )
    
    if factura_id2:
        logica.agregar_producto_factura(factura_id2, producto_ids[1][0], 5)   # 5 Mouse
        logica.agregar_producto_factura(factura_id2, producto_ids[2][0], 2)   # 2 Teclados
        logica.agregar_producto_factura(factura_id2, producto_ids[6][0], 4)   # 4 Webcam
        print(f"  ✓ Factura 2 creada (3 items)")
    
    # Factura 3
    factura_id3 = logica.crear_nueva_factura(
        "Persona Natural",
        nit="1098765432",
        email="cliente@email.com"
    )
    
    if factura_id3:
        logica.agregar_producto_factura(factura_id3, producto_ids[4][0], 1)   # 1 Escritorio
        logica.agregar_producto_factura(factura_id3, producto_ids[7][0], 2)   # 2 Micrófonos
        logica.agregar_producto_factura(factura_id3, producto_ids[8][0], 10)  # 10 Cables
        print(f"  ✓ Factura 3 creada (3 items)")
    
    # ==================== REPORTE ====================
    print("\n" + "="*50)
    print("📊 RESUMEN DE CARGA")
    print("="*50)
    
    stats = logica.obtener_estadisticas()
    
    print(f"\n✅ Productos creados: {stats['total_productos']}")
    print(f"✅ Entradas registradas: {stats['total_entradas']}")
    print(f"✅ Salidas registradas: {stats['total_salidas']}")
    print(f"✅ Facturas generadas: {stats['total_facturas']}")
    print(f"⚠️  Productos bajo stock: {stats['productos_bajo_stock']}")
    print(f"💰 Valor total inventario: ${stats['valor_inventario']:,.2f}")
    
    # Mostrar estado de stock
    print("\n📦 Estado actual de stock:")
    print("-" * 50)
    productos_actuales = logica.obtener_productos()
    for p in productos_actuales:
        estado = "✓" if p['stock'] >= p['stock_minimo'] else "⚠"
        print(f"  {estado} {p['nombre']}: {p['stock']} unidades (mín: {p['stock_minimo']})")
    
    print("\n" + "="*50)
    print("✨ ¡Datos de prueba cargados exitosamente!")
    print("="*50)
    print("\n💡 Próximos pasos:")
    print("   1. Ejecutar: python app.py")
    print("   2. Usar credenciales: admin / 1234")
    print("   3. Explorar las diferentes pestañas")
    print("   4. Generar una factura completa")
    print("   5. Exportar factura (TXT/HTML)")


if __name__ == "__main__":
    cargar_datos_prueba()
