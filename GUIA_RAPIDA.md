# 🚀 INICIO RÁPIDO - CHEAT SHEET

## ⚡ En 30 segundos

```powershell
# 1. Abre PowerShell aquí
# 2. Copia y ejecuta:
python app.py

# 3. Usa: admin / 1234
```

---

## 📱 INTERFAZ - 5 PESTAÑAS

### 1️⃣ PRODUCTOS (📦)
```
Crear nuevo producto:
  Nombre: [_____________]
  Precio: [_____________] $
  Stock: [_____] Mín: [_____]
  [Crear Producto]

Ver lista de todos los productos con stock actual
```

### 2️⃣ ENTRADAS (📥)
```
Registrar compra/reposición:
  Producto: [Selecciona ▼]
  Cantidad: [_____]
  Precio: [_____________]
  Proveedor: [_____________]
  [Registrar Entrada]

Historial de todas las compras
```

### 3️⃣ SALIDAS (📤)
```
Registrar venta:
  Producto: [Selecciona ▼]
  Cantidad: [_____]
  Cliente: [_____________]
  [Crear Factura] [Salida Sin Factura]

Historial de todas las ventas
```

### 4️⃣ FACTURAS (🧾)
```
A) CREAR NUEVA FACTURA:
  Cliente: [________________]
  NIT: [________________]
  Email: [________________]
  Teléfono: [________________]
  [Nueva Factura]

B) AGREGAR PRODUCTOS:
  Producto: [Selecciona ▼]
  Cantidad: [_____]
  [Agregar a Factura]

C) FINALIZAR:
  [Ver Factura] [Guardar TXT] [Guardar HTML]

Listado de todas las facturas creadas
```

### 5️⃣ REPORTES (📊)
```
Estadísticas:
  • Total productos: X
  • Total entradas: Y
  • Total ventas: Z
  • Valor inventario: $XXX,XXX

Productos con Bajo Stock (⚠️):
  - Producto A: 2 unidades (mín: 10)
  - Producto B: 1 unidad (mín: 5)
```

---

## 📋 TAREAS COMUNES

### Crear un Producto
```
1. Ve a pestaña "Productos"
2. Ingresa:
   - Nombre: "Laptop Dell"
   - Precio: 1500000
   - Stock: 5
   - Stock Mín: 2
3. Clic: [Crear Producto]
✓ "Producto creado correctamente"
```

### Registrar una Entrada
```
1. Ve a pestaña "Entradas"
2. Selecciona:
   - Producto: "Laptop Dell"
   - Cantidad: 3
   - Precio: 1400000
   - Proveedor: "Distribuidor ABC"
3. Clic: [Registrar Entrada]
✓ Stock aumenta: 5 → 8
```

### Registrar una Salida
```
1. Ve a pestaña "Salidas"
2. Ingresa:
   - Producto: "Laptop Dell"
   - Cantidad: 1
   - Cliente: "Juan Pérez"
3. Clic: [Salida Sin Factura] O [Crear Factura]
✓ Stock disminuye: 8 → 7
```

### Generar una Factura Completa
```
1. Ve a pestaña "Facturas"
2. Nuevo Cliente:
   - Nombre: "Empresa XYZ"
   - NIT: 9876543210
   - Email: contacto@xyz.com
   - Clic: [Nueva Factura]

3. Agregar Productos:
   - Producto: "Laptop Dell"
   - Cantidad: 1
   - Clic: [Agregar a Factura]
   
   (Repite para más productos)

4. Ver Factura:
   - Clic: [Ver Factura]
   - Se abre ventana con factura

5. Exportar:
   - Clic: [Guardar como TXT] o [Guardar como HTML]
   - ✓ Guardada en carpeta Facturas/
```

### Exportar Factura
```
En ventana de Factura:
  [Guardar como TXT]  → Factura_FAC-20260126-000001.txt
  [Guardar como HTML] → Factura_FAC-20260126-000001.html
  [Cerrar]
```

---

## 💾 DATOS

### Credenciales Predeterminadas
```
Usuario: admin
Contraseña: 1234
```

### Cambiar Contraseña
```powershell
python -c "from database import DatabaseManager; db = DatabaseManager(); c = db.get_connection(); c.execute('UPDATE usuarios SET contraseña=? WHERE usuario=?', ('nueva', 'admin')); c.commit(); print('✓')"
```

### Limpiar Todo (Empezar de Cero)
```powershell
Remove-Item inventario.db
python app.py
```

---

## 📁 ARCHIVOS GENERADOS

Después de usar la app, verás:
```
inventario.db              ← Base de datos
Facturas/
  ├── Factura_FAC-...txt   ← Facturas exportadas
  └── Factura_FAC-...html
```

---

## ⚙️ INSTALACIÓN (Si Necesitas Dependencias)

```powershell
# Para PDF (opcional)
pip install reportlab

# Para todas las opcionales
pip install -r requirements.txt
```

---

## 🐛 PROBLEMAS COMUNES

### "ModuleNotFoundError: No module named 'tkinter'"
```powershell
pip install tk
```

### "inventario.db está bloqueado"
```powershell
# Cierra la app y:
Remove-Item inventario.db
```

### "¿Dónde están mis datos?"
```powershell
# Están en: c:\Users\robin\Documents internos C\App_inventario_local\inventario.db
```

---

## 📊 FÓRMULAS USADAS

**Stock**: Entradas - Salidas

**Subtotal de Factura**: Σ(cantidad × precio)

**IVA**: Subtotal × 19%

**Total**: Subtotal + IVA

---

## 🎯 CHECKLIST DE PRUEBA

Después de instalar, prueba esto:

- [ ] Inicia sesión (admin/1234)
- [ ] Crea 1 producto
- [ ] Registra 1 entrada
- [ ] Registra 1 salida
- [ ] Crea 1 factura con 2 productos
- [ ] Exporta factura a TXT
- [ ] Exporta factura a HTML
- [ ] Ve los reportes
- [ ] Verifica stock automático

Si todo funciona → ¡Listo para usar! 🎉

---

## 📞 AYUDA RÁPIDA

| Problema | Solución |
|----------|----------|
| Olvide contraseña | Ver sección "Cambiar Contraseña" |
| Necesito más usuarios | Usa admin para crear nuevos |
| Perdí datos | Recupera del backup de inventario.db |
| Quiero empezar de cero | Borra inventario.db |
| No funciona GUI | Instala Python 3.8+ con tkinter |

---

## 🚀 PRÓXIMO PASO

```powershell
python app.py
```

**¡Y comienza a gestionar tu inventario!** 📊
