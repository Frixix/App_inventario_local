# 📋 GUÍA DE INSTALACIÓN Y EJECUCIÓN

## ✅ Requisitos Previos

- **Python 3.8+** (ya debería estar instalado)
- **tkinter** (viene incluido con Python en Windows)

## 🚀 Pasos para Ejecutar

### Opción 1: Ejecución Directa (Recomendado)

1. **Abre PowerShell en la carpeta del proyecto**
   ```powershell
   # Navega a la carpeta
   cd "c:\Users\robin\Documents internos C\App_inventario_local"
   ```

2. **Ejecuta la aplicación**
   ```powershell
   python app.py
   ```

3. **Inicia sesión** con:
   - Usuario: `admin`
   - Contraseña: `1234`

### Opción 2: Con Datos de Prueba

1. **Carga primero los datos de ejemplo** (opcional pero recomendado):
   ```powershell
   python prueba_datos.py
   ```

2. **Luego ejecuta la aplicación**:
   ```powershell
   python app.py
   ```

---

## 📦 Archivos del Proyecto

```
App_inventario_local/
├── app.py                      ← Punto de entrada (EJECUTAR ESTO)
├── interfaz.py                 ← GUI (Capa de Interfaz)
├── logica.py                   ← Lógica de negocio (Capa Lógica)
├── database.py                 ← Base de datos SQLite (Capa Datos)
├── facturas.py                 ← Generación de facturas
├── prueba_datos.py             ← Script para cargar datos de ejemplo
├── inventario.db               ← Base de datos (se crea automáticamente)
├── README.md                   ← Documentación general
├── FACTURA_ELECTRONICA.md      ← Documentación factura electrónica
└── INSTALACION.md              ← Este archivo
```

---

## 🎯 Flujo de Uso Recomendado

### Primera vez:
```
1. python prueba_datos.py    (Carga datos de ejemplo)
2. python app.py             (Abre la aplicación)
3. Inicia sesión: admin/1234
4. Explora las 5 pestañas
5. Genera una factura
6. Exporta como TXT o HTML
```

### Uso normal:
```
1. python app.py             (Abre la aplicación)
2. Inicia sesión
3. Gestiona inventario
```

---

## ⚙️ Configuración (Opcional)

### Cambiar Credenciales de Admin

Abre PowerShell y ejecuta:
```powershell
python -c "from database import DatabaseManager; db = DatabaseManager(); conn = db.get_connection(); conn.execute('UPDATE usuarios SET contraseña=? WHERE usuario=?', ('nueva_contraseña', 'admin')); conn.commit(); conn.close(); print('✓ Contraseña actualizada')"
```

### Limpiar Base de Datos (Empezar de cero)

```powershell
# Elimina el archivo de base de datos
Remove-Item inventario.db

# Corre la app para crear una nueva BD vacía
python app.py
```

---

## 🐛 Solución de Problemas

### Problema: "No module named 'tkinter'"
**Solución**: Tkinter debería venir incluido. Si no:
```powershell
# En Windows, reinstala Python con opción tcl/tk marcada
# O instala:
pip install tk
```

### Problema: "Port already in use"
**Solución**: Cierra otras instancias de la aplicación

### Problema: "Permission denied inventario.db"
**Solución**: 
```powershell
# Cierra la aplicación y abre PowerShell como administrador
# Luego ejecuta:
python app.py
```

### Problema: La base de datos está corrupta
**Solución**: Elimina el archivo `inventario.db` (se recreará)

---

## 📊 Funcionalidades Principales

| Pestaña | Función |
|---------|---------|
| 📦 Productos | Crear productos, ver stock, alertas de bajo stock |
| 📥 Entradas | Registrar compras/reposición |
| 📤 Salidas | Registrar ventas |
| 🧾 Facturas | Crear, agregar items, ver y exportar facturas |
| 📊 Reportes | Estadísticas, productos bajo stock |

---

## 💾 Respaldo de Datos

Para hacer backup de tu inventario:

```powershell
# En PowerShell, copia el archivo de BD
Copy-Item inventario.db "inventario_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
```

---

## 🔄 Actualizar/Distribuir la Aplicación

Para compartir la app con otros usuarios:

1. **Copia la carpeta completa** (menos `inventario.db` si es nueva)
2. **Comparte con otros** vía USB, email, drive, etc.
3. **Cada usuario** ejecuta: `python app.py`

**Nota**: Cada instalación tendrá su propia base de datos local

---

## 📞 Soporte Rápido

**Si algo no funciona:**
1. Verifica que tienes Python 3.8+ instalado: `python --version`
2. Verifica que estás en la carpeta correcta: `ls` o `dir`
3. Intenta eliminar `inventario.db` y ejecutar de nuevo
4. Revisa los archivos de la carpeta

---

## ✨ Próximas Mejoras

- [ ] Sincronización en la nube
- [ ] Integración con email para facturas
- [ ] Módulo contable
- [ ] Integración DIAN real
- [ ] Acceso multi-usuario en red
- [ ] App móvil complementaria

---

**¡Listo para usar! 🎉**

Ejecuta en PowerShell:
```powershell
cd "c:\Users\robin\Documents internos C\App_inventario_local"
python app.py
```
