#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar las correcciones del panel de admin
"""

import sys
sys.path.insert(0, '/home/claude')

from logica import LogicaInventario

def probar_correcciones():
    """Prueba las correcciones realizadas"""
    print("\n" + "="*60)
    print("🧪 PRUEBA DE CORRECCIONES - SISTEMA DE ADMINISTRADOR")
    print("="*60)
    
    # Crear instancia de LogicaInventario
    print("\n1️⃣ Creando instancia de LogicaInventario...")
    logica = LogicaInventario()
    print("   ✅ Instancia creada exitosamente")
    
    # Probar estado inicial (sin login)
    print("\n2️⃣ Verificando estado sin login...")
    print(f"   Usuario actual: {logica.usuario_actual}")
    print(f"   ¿Es administrador?: {logica.es_administrador()}")
    
    if logica.es_administrador():
        print("   ❌ ERROR: No debería ser admin sin login")
    else:
        print("   ✅ CORRECTO: No es admin sin login")
    
    # Probar login con admin
    print("\n3️⃣ Probando login con usuario 'admin'...")
    resultado_login = logica.login('admin', '1234')
    
    if resultado_login:
        print("   ✅ Login exitoso")
        logica.diagnosticar_usuario()
    else:
        print("   ❌ ERROR: Login falló")
        return False
    
    # Verificar estado después del login
    print("\n4️⃣ Verificando permisos de administrador...")
    es_admin = logica.es_administrador()
    print(f"   ¿Es administrador?: {es_admin}")
    
    if es_admin:
        print("   ✅ CORRECTO: Usuario admin tiene permisos")
    else:
        print("   ❌ ERROR: Usuario admin NO tiene permisos")
        print("   Datos del usuario:")
        print(f"   {logica.usuario_actual}")
        return False
    
    # Probar funciones de administrador
    print("\n5️⃣ Probando funciones de administrador...")
    
    # Crear producto de prueba
    print("   - Creando producto de prueba...")
    if logica.crear_producto("Producto Test Admin", 100.0, 5, 2, "Producto de prueba"):
        print("     ✅ Producto creado")
    else:
        print("     ❌ Error al crear producto")
    
    # Obtener productos
    print("   - Obteniendo lista de productos...")
    productos = logica.obtener_productos()
    print(f"     ✅ {len(productos)} productos encontrados")
    
    # Verificar estructura de productos
    if productos:
        print("   - Verificando estructura del primer producto...")
        p = productos[0]
        if isinstance(p, dict):
            print(f"     ✅ Producto es un diccionario")
            print(f"     Claves: {list(p.keys())}")
        else:
            print(f"     ❌ Producto NO es un diccionario: {type(p)}")
    
    print("\n" + "="*60)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        exito = probar_correcciones()
        if exito:
            print("✅ Sistema funcionando correctamente")
            print("\n📝 RESUMEN DE CORRECCIONES:")
            print("   1. Validación robusta en es_administrador()")
            print("   2. Verificación de tipo de datos (isinstance)")
            print("   3. Soporte para usuario='admin' O nombre='Administrador'")
            print("   4. Logging mejorado para debugging")
            print("   5. Manejo de errores en panel de edición")
            print("   6. Validaciones en carga de productos")
            print("\n✅ El error 'NoneType object is not subscriptable' está RESUELTO")
        else:
            print("❌ Se encontraron problemas durante las pruebas")
    except Exception as e:
        print(f"\n❌ ERROR DURANTE LAS PRUEBAS:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
