# Parámetros de Factura Electrónica Colombia (DIAN)

## 📋 Campos Obligatorios Factura Electrónica (Referencia DIAN)

### 1. Identificación de la Factura
- ✅ **Número de factura única** - FAC-YYYYMMDD-000001
- ✅ **Fecha de emisión** - YYYY-MM-DD HH:MM:SS
- ✅ **Hora de emisión** - HH:MM:SS

### 2. Datos del Vendedor (Emisor)
- ✅ **Razón social**
- ✅ **NIT**
- ✅ **Dígito de verificación NIT**
- ✅ **Dirección**
- ✅ **Ciudad / Municipio**
- ✅ **Código DIAN municipio** (opcional para fase inicial)
- ✅ **Teléfono** (opcional)
- ✅ **Email** (opcional)
- ✅ **País** (CO)

### 3. Datos del Cliente (Adquirente)
- ✅ **Tipo documento** (CC, NIT, CE, etc.)
- ✅ **Número documento**
- ✅ **Nombre/Razón social**
- ✅ **Dirección** (opcional)
- ✅ **Teléfono** (opcional)
- ✅ **Email** (opcional)

### 4. Descripción de Productos/Servicios
- ✅ **Código del artículo** (opcional, pero recomendado)
- ✅ **Descripción del producto**
- ✅ **Cantidad**
- ✅ **Unidad de medida** (UN, KG, MTS, etc.)
- ✅ **Precio unitario**
- ✅ **Descuento por línea** (opcional)
- ✅ **Subtotal línea**

### 5. Cálculo de Valores
- ✅ **Subtotal** (suma de todos los items)
- ✅ **Descuento total** (opcional)
- ✅ **Base imponible IVA**
- ✅ **IVA** (19% estándar, o según aplique)
- ✅ **Impuesto al consumo** (opcional)
- ✅ **Retención en la fuente** (opcional)
- ✅ **Total a pagar**

### 6. Información Adicional
- ⚠️ **Medio de pago** (efectivo, cheque, transferencia, etc.)
- ⚠️ **Notas o comentarios**
- ⚠️ **Referencia de factura anterior** (si es ajuste)
- ⚠️ **Período facturado** (si aplica)

---

## 🏗️ Estructura Implementada en la App

### ✅ YA IMPLEMENTADO:

```python
# En database.py - Tabla facturas
facturas {
    numero_factura:     "FAC-20260126-000001"
    fecha:              "2026-01-26 14:30:00"
    
    # VENDEDOR (datos estáticos por ahora)
    # vendedor_nombre:  "Mi Empresa"
    # vendedor_nit:     "123456789"
    
    # CLIENTE
    cliente_nombre:     "Juan Pérez"
    cliente_nit:        "1234567890"
    cliente_email:      "juan@example.com"
    cliente_telefono:   "3001234567"
    
    # VALORES
    subtotal:           150000.00
    iva_porcentaje:     19
    iva_valor:          28500.00
    total:              178500.00
    
    # ADICIONAL
    notas:              "Observaciones adicionales"
    estado:             "Activa"
}

# Salidas (items de factura)
salidas {
    producto_id:        1
    cantidad:           5
    precio_unitario:    30000.00
    # subtotal = 150000.00
    factura_id:         1
}
```

---

## 🚀 Próximas Mejoras (Fase 2)

### Para Factura Real DIAN:

1. **Datos del Vendedor Configurables**
   ```python
   # Agregar tabla: configuracion_empresa
   config = {
       'razon_social': 'Mi Empresa SAS',
       'nit': '123456789',
       'dv_nit': '0',
       'direccion': 'Cll 123 #45-67',
       'ciudad': 'Bogotá',
       'codigo_dian_municipio': '11001',
       'telefono': '601234567',
       'email': 'empresa@example.com',
       'pais': 'CO'
   }
   ```

2. **Tipos de Documento Estandarizados**
   ```python
   TIPOS_DOCUMENTO = {
       'CC': 'Cédula Ciudadanía',
       'NIT': 'NIT',
       'CE': 'Cédula Extranjería',
       'TI': 'Tarjeta Identidad',
       'PP': 'Pasaporte'
   }
   ```

3. **Unidades de Medida DIAN**
   ```python
   UNIDADES_MEDIDA = {
       'UN': 'Unidad',
       'KG': 'Kilogramo',
       'MTS': 'Metro',
       'LT': 'Litro',
       'GALÓN': 'Galón',
       'CAJA': 'Caja',
       'PAQ': 'Paquete'
   }
   ```

4. **Medios de Pago**
   ```python
   MEDIOS_PAGO = {
       '1': 'Efectivo',
       '2': 'Cheque',
       '3': 'Transferencia Bancaria',
       '4': 'Tarjeta Débito',
       '5': 'Tarjeta Crédito',
       '6': 'Crédito',
       '7': 'Bonos'
   }
   ```

5. **Códigos DIAN Municipios**
   ```python
   # Para Bogotá: 11001
   # Para Medellín: 05001
   # Etc.
   ```

---

## 📊 Ejemplo de Factura Generada

```
============================================================
FACTURA ELECTRÓNICA
============================================================

Número: FAC-20260126-000001
Fecha: 2026-01-26 14:30:00

VENDEDOR:
Nombre: Mi Empresa
NIT: 123456789
Email: empresa@example.com

CLIENTE:
Nombre: Juan Pérez
NIT: 1234567890
Email: juan@example.com
Teléfono: 3001234567

------------------------------------------------------------
PRODUCTO                       CANTIDAD    PRECIO   SUBTOTAL
------------------------------------------------------------
Producto A                            5  $30000.00 $150000.00
------------------------------------------------------------

Subtotal:     $150000.00
IVA (19%):     $28500.00
============================================================
TOTAL:        $178500.00
============================================================

Gracias por su compra
```

---

## 🔐 Consideraciones para DIAN Real

### NO IMPLEMENTADO (Fase Futura):
- ❌ Firma digital con certificado (XSD)
- ❌ Validación contra servicios DIAN
- ❌ Cúfe (Código único de facturación electrónica)
- ❌ QR obligatorio
- ❌ Conexión a servidor DIAN

### FASE INICIAL (Educativa/Funcional):
- ✅ Estructura de datos correcta
- ✅ Cálculos de IVA
- ✅ Generación de números de factura únicos
- ✅ Exportación en TXT y HTML
- ✅ PDF (opcional con reportlab)

---

## 📚 Referencias

**DIAN - Colombia:**
- https://www.dian.gov.co/
- Resolución 000042 de 2020
- Resolución 000039 de 2021

**Para fase real:**
1. Registrarse como productor de FE en DIAN
2. Obtener certificado digital
3. Conectar con Software Habilitado (SH) certificado
4. Implementar validaciones XSD
5. Generar CÚFE y QR

---

## 🎯 Estado Actual

**✅ Fase 1 (Actual):** Factura educativa y funcional
**⏳ Fase 2 (Próxima):** Integración DIAN real

¡La app está lista para gestión interna y educación sobre facturas!
