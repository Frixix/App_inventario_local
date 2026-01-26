-- ESQUEMA DE BASE DE DATOS - SISTEMA DE INVENTARIO LOCAL
-- Tipo: SQLite3
-- Archivo: inventario.db

-- ============================================================
-- TABLA: USUARIOS
-- Descripción: Datos de usuarios del sistema
-- ============================================================

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT UNIQUE NOT NULL,
    contraseña TEXT NOT NULL,
    nombre TEXT NOT NULL,
    email TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índice para búsqueda rápida
CREATE UNIQUE INDEX idx_usuario_login ON usuarios(usuario);

-- Usuario predeterminado (insertar en init_database)
-- INSERT INTO usuarios VALUES (1, 'admin', '1234', 'Administrador', 'admin@inventario.local', CURRENT_TIMESTAMP);


-- ============================================================
-- TABLA: PRODUCTOS
-- Descripción: Catálogo de productos
-- ============================================================

CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    precio REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 10,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_producto_nombre ON productos(nombre);
CREATE INDEX idx_producto_stock ON productos(stock);


-- ============================================================
-- TABLA: ENTRADAS
-- Descripción: Registro de entradas (compras/reposición)
-- ============================================================

CREATE TABLE entradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    proveedor TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id INTEGER,
    FOREIGN KEY(producto_id) REFERENCES productos(id),
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);

-- Índices
CREATE INDEX idx_entrada_producto ON entradas(producto_id);
CREATE INDEX idx_entrada_fecha ON entradas(fecha);
CREATE INDEX idx_entrada_usuario ON entradas(usuario_id);


-- ============================================================
-- TABLA: SALIDAS
-- Descripción: Registro de salidas (ventas)
-- ============================================================

CREATE TABLE salidas (
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
);

-- Índices
CREATE INDEX idx_salida_producto ON salidas(producto_id);
CREATE INDEX idx_salida_fecha ON salidas(fecha);
CREATE INDEX idx_salida_usuario ON salidas(usuario_id);
CREATE INDEX idx_salida_factura ON salidas(factura_id);


-- ============================================================
-- TABLA: FACTURAS
-- Descripción: Registro de facturas electrónicas
-- ============================================================

CREATE TABLE facturas (
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
);

-- Índices
CREATE UNIQUE INDEX idx_factura_numero ON facturas(numero_factura);
CREATE INDEX idx_factura_fecha ON facturas(fecha);
CREATE INDEX idx_factura_cliente ON facturas(cliente_nombre);
CREATE INDEX idx_factura_estado ON facturas(estado);


-- ============================================================
-- VISTAS ÚTILES
-- ============================================================

-- Vista: Resumen de factura con items
CREATE VIEW v_factura_resumen AS
SELECT 
    f.id,
    f.numero_factura,
    f.fecha,
    f.cliente_nombre,
    f.cliente_nit,
    COUNT(s.id) as cantidad_items,
    SUM(s.cantidad * s.precio_unitario - COALESCE(s.descuento, 0)) as subtotal,
    f.total,
    f.estado
FROM 
    facturas f
    LEFT JOIN salidas s ON f.id = s.factura_id
GROUP BY 
    f.id;


-- Vista: Movimientos por producto
CREATE VIEW v_movimientos_producto AS
SELECT 
    p.id,
    p.nombre,
    p.precio,
    p.stock,
    (SELECT SUM(cantidad) FROM entradas WHERE producto_id = p.id) as total_entradas,
    (SELECT SUM(cantidad) FROM salidas WHERE producto_id = p.id) as total_salidas
FROM 
    productos p;


-- Vista: Productos bajo stock
CREATE VIEW v_productos_bajo_stock AS
SELECT 
    id,
    nombre,
    stock,
    stock_minimo,
    (stock_minimo - stock) as unidades_faltantes
FROM 
    productos
WHERE 
    stock < stock_minimo
ORDER BY 
    unidades_faltantes DESC;


-- ============================================================
-- CONSULTAS ÚTILES PARA REPORTES
-- ============================================================

-- Reporte 1: Ventas totales por mes
-- SELECT 
--     strftime('%Y-%m', f.fecha) as mes,
--     COUNT(f.id) as cantidad_facturas,
--     SUM(f.total) as total_ventas
-- FROM facturas f
-- WHERE f.estado = 'Activa'
-- GROUP BY strftime('%Y-%m', f.fecha)
-- ORDER BY mes DESC;


-- Reporte 2: Productos más vendidos
-- SELECT 
--     p.nombre,
--     SUM(s.cantidad) as total_vendido,
--     SUM(s.cantidad * s.precio_unitario) as total_ingresos
-- FROM salidas s
-- JOIN productos p ON s.producto_id = p.id
-- GROUP BY p.id
-- ORDER BY total_vendido DESC
-- LIMIT 10;


-- Reporte 3: Valor total del inventario
-- SELECT 
--     SUM(stock * precio) as valor_inventario,
--     COUNT(*) as cantidad_productos,
--     AVG(precio) as precio_promedio,
--     SUM(CASE WHEN stock < stock_minimo THEN 1 ELSE 0 END) as productos_bajo_stock
-- FROM productos;


-- Reporte 4: Clientes principales
-- SELECT 
--     cliente_nombre,
--     COUNT(*) as cantidad_facturas,
--     SUM(total) as monto_total,
--     AVG(total) as ticket_promedio
-- FROM facturas
-- WHERE estado = 'Activa'
-- GROUP BY cliente_nombre
-- ORDER BY monto_total DESC
-- LIMIT 10;


-- ============================================================
-- TRIGGERS (Automáticos)
-- ============================================================

-- Trigger: Actualizar stock al insertar entrada
CREATE TRIGGER tg_entrada_actualizar_stock
AFTER INSERT ON entradas
BEGIN
  UPDATE productos 
  SET stock = stock + NEW.cantidad
  WHERE id = NEW.producto_id;
END;


-- Trigger: Actualizar stock al insertar salida
CREATE TRIGGER tg_salida_actualizar_stock
AFTER INSERT ON salidas
BEGIN
  UPDATE productos 
  SET stock = stock - NEW.cantidad
  WHERE id = NEW.producto_id;
END;


-- ============================================================
-- DATOS DE EJEMPLO (OPCIONAL)
-- ============================================================

-- Insertar productos de ejemplo
-- INSERT INTO productos (nombre, precio, stock, stock_minimo, descripcion)
-- VALUES 
--     ('Laptop Dell', 1500000, 5, 2, 'Laptop para desarrollo'),
--     ('Mouse Logitech', 45000, 20, 5, 'Mouse inalámbrico'),
--     ('Teclado Mecánico', 250000, 10, 3, 'Teclado RGB');


-- ============================================================
-- RESUMEN DEL ESQUEMA
-- ============================================================
/*

TABLA            RELACIONES              PROPÓSITO
─────────────────────────────────────────────────────────────
usuarios         (PK: id)                Autenticación
productos        (PK: id)                Catálogo
entradas         (FK: producto_id)       Compras/Reposición
salidas          (FK: producto_id)       Ventas
                 (FK: factura_id)
facturas         (FK: usuario_id)        Facturación

FLUJO:
1. Usuario se autentica (tabla usuarios)
2. Crea/Registra productos (tabla productos)
3. Registra entradas (compras) → Aumenta stock
4. Registra salidas (ventas) → Disminuye stock
5. Crea factura → Agrega items de salidas

*/

-- ============================================================
-- INFORMACIÓN TÉCNICA
-- ============================================================

/*
BASE DE DATOS: SQLite3
TIPO: Relacional normalizado
ARCHIVO: inventario.db
TAMAÑO: < 1 MB (típicamente)

VENTAJAS SQLite PARA ESTA APP:
✓ Sin servidor
✓ Archivo único y portátil
✓ Transacciones ACID
✓ Completamente funcional
✓ Fácil de hacer backup
✓ Compatible con Python nativo

SEGURIDAD:
✓ Parametrización (evita SQL injection)
✓ Transacciones atómicas
✓ Integridad referencial (FK)
✓ Índices para rendimiento
✓ Triggers automáticos

ESCALABILIDAD (FUTURO):
Si necesita más de 100 usuarios simultáneos:
→ Migrar a PostgreSQL/MySQL (cambio en database.py)

*/
