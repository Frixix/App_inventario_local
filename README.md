# 🏪 Sistema de Inventario Local - Documentación

## Descripción General

Aplicación de escritorio para gestión de inventario con interfaz de 3 capas (Interfaz, Lógica, Datos). Permite:

-  Gestión de productos (crear, ver stock)
-  Registrar entradas (compras/reposición)
-  Registrar salidas (ventas)
-  Generación de facturas electrónicas
-  Reportes y estadísticas
-  Base de datos SQLite integrada

---

##  Estructura de 3 Capas

```
┌─────────────────────────────────────┐
│   CAPA DE INTERFAZ (interfaz.py)    │  ← GUI con tkinter
├─────────────────────────────────────┤
│   CAPA DE LÓGICA (logica.py)        │  ← Reglas de negocio
├─────────────────────────────────────┤
│   CAPA DE DATOS (database.py)       │  ← SQLite
└─────────────────────────────────────┘
```

### Capa de Interfaz (interfaz.py)
- Interfaz gráfica con tkinter
- 5 pestañas principales: Productos, Entradas, Salidas, Facturas, Reportes
- Sistema de login predeterminado (admin/1234)

### Capa de Lógica (logica.py)
- Clase `LogicaInventario` con métodos de negocio
- Validaciones y cálculos
- Manejo de usuarios y autenticación

### Capa de Datos (database.py)
- Clase `DatabaseManager` para SQLite
- Tablas: usuarios, productos, entradas, salidas, facturas
- CRUD completo para cada entidad

---

##  Base de Datos - Esquema

### Tabla: usuarios
```sql
id          INTEGER PRIMARY KEY
usuario     TEXT UNIQUE NOT NULL
contraseña  TEXT NOT NULL
nombre      TEXT NOT NULL
email       TEXT
fecha_creacion TIMESTAMP
```

**Usuario predeterminado:**
- Usuario: `admin`
- Contraseña: `1234`

### Tabla: productos
```sql
id              INTEGER PRIMARY KEY
nombre          TEXT UNIQUE NOT NULL
precio          REAL NOT NULL
stock           INTEGER DEFAULT 0
stock_minimo    INTEGER DEFAULT 10
descripcion     TEXT
fecha_creacion  TIMESTAMP
```

### Tabla: entradas
```sql
id              INTEGER PRIMARY KEY
producto_id     INTEGER FOREIGN KEY
cantidad        INTEGER NOT NULL
precio_unitario REAL NOT NULL
proveedor       TEXT
fecha           TIMESTAMP
usuario_id      INTEGER FOREIGN KEY
```

### Tabla: salidas
```sql
id              INTEGER PRIMARY KEY
producto_id     INTEGER FOREIGN KEY
cantidad        INTEGER NOT NULL
precio_unitario REAL NOT NULL
descuento       REAL DEFAULT 0
cliente         TEXT
fecha           TIMESTAMP
usuario_id      INTEGER FOREIGN KEY
factura_id      INTEGER FOREIGN KEY
```

### Tabla: facturas
```sql
id                  INTEGER PRIMARY KEY
numero_factura      TEXT UNIQUE NOT NULL
fecha               TIMESTAMP
cliente_nombre      TEXT NOT NULL
cliente_nit         TEXT
cliente_email       TEXT
cliente_telefono    TEXT
subtotal            REAL DEFAULT 0
descuento_total     REAL DEFAULT 0
iva_porcentaje      REAL DEFAULT 19
iva_valor           REAL DEFAULT 0
total               REAL DEFAULT 0
usuario_id          INTEGER FOREIGN KEY
notas               TEXT
estado              TEXT DEFAULT 'Activa'
```

---

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.8+
- tkinter (incluido en Python)

### Instalación
```bash
# El archivo inventario.db se crea automáticamente
python app.py
```

### Credenciales de Prueba
```
Usuario: admin
Contraseña: 1234
```

---

##  Guía de Uso

### 1️ Productos
- **Crear Producto**: Ingrese nombre, precio, stock inicial y stock mínimo
- El sistema alerta cuando el stock está bajo
- Lista actualizada en tiempo real

### 2️ Entradas (Compras/Reposición)
- Seleccione producto de la lista
- Ingrese cantidad y precio unitario
- Ingrese nombre del proveedor (opcional)
- El stock se actualiza automáticamente

### 3️ Salidas (Ventas)
- Seleccione producto de la lista
- Ingrese cantidad a vender
- Ingrese nombre del cliente (opcional)
- El sistema verifica stock disponible

### 4️ Facturas
**Dos opciones:**

**Opción A: Factura paso a paso**
1. Haga clic en "Nueva Factura"
2. Ingrese datos del cliente (Nombre, NIT, Email, Teléfono)
3. Agregue productos uno a uno
4. Haga clic en "Ver Factura" para visualizar
5. Guarde como TXT o HTML

**Opción B: Factura rápida desde Salidas**
1. En la pestaña Salidas, ingrese datos
2. Haga clic en "Crear Factura"
3. Se crea factura con el producto

### 5️ Reportes
- Estadísticas generales
- Productos bajo stock (con alertas)
- Botón de actualización

---

##  Factura Electrónica - Parámetros Incluidos

 Número único (FAC-YYYYMMDD-000001)  
 Fecha de emisión  
 Datos del vendedor (empresa)  
 Datos del cliente  
 Productos y cantidades  
 Precios unitarios  
 Subtotal  
 IVA (19% por defecto, configurable)  
 Total  

**Formatos de exportación:**
- TXT (texto simple)
- HTML (visualización web)
- PDF (requiere `pip install reportlab`)

---

##  Archivos Generados

### Base de Datos
- `inventario.db` - SQLite (se crea automáticamente)

### Facturas
- Carpeta `Facturas/` - Almacena TXT y HTML
- Nombre: `Factura_FAC-YYYYMMDD-000001.txt|html`

---

##  Consideraciones de Seguridad

### Para producción:
- Cambiar credenciales predeterminadas
- Encriptar contraseñas (bcrypt, argon2)
- Implementar roles y permisos
- Auditoría de operaciones
- Backups automáticos de BD

### Código para cambiar contraseña admin:
```python
from database import DatabaseManager

db = DatabaseManager()
db.db.execute("UPDATE usuarios SET contraseña=? WHERE usuario='admin'", ("nueva_pass",))
db.db.commit()
```

---

##  Extensiones Futuras

### Fase 2:
- [ ] Integración con DIAN (factura electrónica real)
- [ ] Módulo de cuentas por cobrar
- [ ] Inventario por sucursal
- [ ] Integración de pagos

### Fase 3:
- [ ] Sincronización en la nube
- [ ] App móvil (complementaria)
- [ ] Reportes avanzados en PDF
- [ ] Integración con contabilidad

### Fase 4:
- [ ] Machine Learning para pronósticos
- [ ] Dashboard web
- [ ] API REST

---

##  Contacto y Soporte

Para cambios o mejoras, modifique los archivos correspondientes:
- **Interfaz**: `interfaz.py`
- **Lógica**: `logica.py`
- **Base de datos**: `database.py`
- **Facturas**: `facturas.py`

---

##  Checklist de Implementación

✅ Sistema de login con usuario/contraseña  
✅ Gestión de productos (CRUD)  
✅ Módulo de entradas  
✅ Módulo de salidas  
✅ Stock automático  
✅ Generación de facturas  
✅ Parámetros de factura electrónica  
✅ Base de datos SQLite  
✅ Interfaz de 3 capas  
✅ Exportación de facturas (TXT/HTML)  

---


