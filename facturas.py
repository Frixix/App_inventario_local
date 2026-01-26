"""
Utilidades para generación de facturas (PDF y visualización)
"""

from datetime import datetime
from logica import LogicaInventario

class GeneradorFactura:
    """Clase para generar facturas en texto o exportarlas"""
    
    def __init__(self, logica):
        self.logica = logica
    
    def generar_texto_factura(self, factura_id):
        """Genera la factura en formato texto"""
        resumen = self.logica.generar_resumen_factura(factura_id)
        
        if not resumen:
            return None
        
        lineas = []
        lineas.append("=" * 60)
        lineas.append("FACTURA ELECTRÓNICA".center(60))
        lineas.append("=" * 60)
        lineas.append("")
        
        # Datos de la factura
        lineas.append(f"Número: {resumen['numero']}")
        lineas.append(f"Fecha: {resumen['fecha']}")
        lineas.append("")
        
        # Datos del vendedor (estático por ahora)
        lineas.append("VENDEDOR:")
        lineas.append("Nombre: Mi Empresa")
        lineas.append("NIT: 123456789")
        lineas.append("Email: empresa@example.com")
        lineas.append("")
        
        # Datos del cliente
        lineas.append("CLIENTE:")
        lineas.append(f"Nombre: {resumen['cliente']['nombre']}")
        if resumen['cliente']['nit']:
            lineas.append(f"NIT: {resumen['cliente']['nit']}")
        if resumen['cliente']['email']:
            lineas.append(f"Email: {resumen['cliente']['email']}")
        if resumen['cliente']['telefono']:
            lineas.append(f"Teléfono: {resumen['cliente']['telefono']}")
        lineas.append("")
        
        # Encabezado de items
        lineas.append("-" * 60)
        lineas.append(f"{'PRODUCTO':<25} {'CANTIDAD':>8} {'PRECIO':>10} {'SUBTOTAL':>10}")
        lineas.append("-" * 60)
        
        # Items
        for item in resumen['items']:
            producto = item['nombre']
            cantidad = item['cantidad']
            precio = item['precio_unitario']
            subtotal = cantidad * precio
            
            lineas.append(
                f"{producto:<25} {cantidad:>8} ${precio:>9.2f} ${subtotal:>9.2f}"
            )
        
        lineas.append("-" * 60)
        
        # Totales
        lineas.append("")
        lineas.append(f"Subtotal:     ${resumen['subtotal']:>12.2f}")
        lineas.append(f"IVA ({resumen['iva_porcentaje']}%):  ${resumen['iva_valor']:>12.2f}")
        lineas.append("=" * 60)
        lineas.append(f"TOTAL:        ${resumen['total']:>12.2f}")
        lineas.append("=" * 60)
        lineas.append("")
        lineas.append("Gracias por su compra".center(60))
        
        return "\n".join(lineas)
    
    def guardar_factura_txt(self, factura_id, ruta=None):
        """Guarda la factura en formato TXT"""
        factura = self.logica.obtener_factura(factura_id)
        if not factura:
            return False
        
        texto = self.generar_texto_factura(factura_id)
        
        if ruta is None:
            ruta = f"Facturas/Factura_{factura['numero_factura']}.txt"
        
        try:
            import os
            os.makedirs(os.path.dirname(ruta) or '.', exist_ok=True)
            
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(texto)
            
            return True
        except Exception as e:
            print(f"Error al guardar factura: {e}")
            return False
    
    def generar_factura_html(self, factura_id):
        """Genera la factura en formato HTML"""
        resumen = self.logica.generar_resumen_factura(factura_id)
        
        if not resumen:
            return None
        
        items_html = ""
        for item in resumen['items']:
            subtotal = item['cantidad'] * item['precio_unitario']
            items_html += f"""
            <tr>
                <td>{item['nombre']}</td>
                <td class="numero">{item['cantidad']}</td>
                <td class="numero">${item['precio_unitario']:.2f}</td>
                <td class="numero">${subtotal:.2f}</td>
            </tr>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Factura {resumen['numero']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            color: #333;
        }}
        .header p {{
            margin: 5px 0;
            color: #666;
        }}
        .info-section {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .info-box {{
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 4px;
        }}
        .info-box h3 {{
            margin-top: 0;
            color: #333;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }}
        .info-box p {{
            margin: 5px 0;
            color: #666;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th {{
            background-color: #f0f0f0;
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
            font-weight: bold;
        }}
        td {{
            padding: 10px;
            border: 1px solid #ddd;
        }}
        .numero {{
            text-align: right;
        }}
        .totales {{
            margin-top: 20px;
            margin-left: auto;
            width: 300px;
        }}
        .total-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #ddd;
        }}
        .total-row.final {{
            border-bottom: 2px solid #333;
            border-top: 2px solid #333;
            font-weight: bold;
            font-size: 1.2em;
            padding: 12px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>FACTURA ELECTRÓNICA</h1>
            <p>Número: {resumen['numero']}</p>
            <p>Fecha: {resumen['fecha']}</p>
        </div>
        
        <div class="info-section">
            <div class="info-box">
                <h3>VENDEDOR</h3>
                <p><strong>Nombre:</strong> Mi Empresa</p>
                <p><strong>NIT:</strong> 123456789</p>
                <p><strong>Email:</strong> empresa@example.com</p>
            </div>
            
            <div class="info-box">
                <h3>CLIENTE</h3>
                <p><strong>Nombre:</strong> {resumen['cliente']['nombre']}</p>
                {f"<p><strong>NIT:</strong> {resumen['cliente']['nit']}</p>" if resumen['cliente']['nit'] else ""}
                {f"<p><strong>Email:</strong> {resumen['cliente']['email']}</p>" if resumen['cliente']['email'] else ""}
                {f"<p><strong>Teléfono:</strong> {resumen['cliente']['telefono']}</p>" if resumen['cliente']['telefono'] else ""}
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Producto</th>
                    <th class="numero">Cantidad</th>
                    <th class="numero">Precio Unitario</th>
                    <th class="numero">Subtotal</th>
                </tr>
            </thead>
            <tbody>
                {items_html}
            </tbody>
        </table>
        
        <div class="totales">
            <div class="total-row">
                <span>Subtotal:</span>
                <span>${resumen['subtotal']:.2f}</span>
            </div>
            <div class="total-row">
                <span>IVA ({resumen['iva_porcentaje']}%):</span>
                <span>${resumen['iva_valor']:.2f}</span>
            </div>
            <div class="total-row final">
                <span>TOTAL:</span>
                <span>${resumen['total']:.2f}</span>
            </div>
        </div>
        
        <div class="footer">
            <p>Gracias por su compra</p>
            <p style="font-size: 0.9em; color: #999;">Esta factura fue generada automáticamente por el sistema de inventario</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def guardar_factura_html(self, factura_id, ruta=None):
        """Guarda la factura en formato HTML"""
        factura = self.logica.obtener_factura(factura_id)
        if not factura:
            return False
        
        html = self.generar_factura_html(factura_id)
        
        if ruta is None:
            ruta = f"Facturas/Factura_{factura['numero_factura']}.html"
        
        try:
            import os
            os.makedirs(os.path.dirname(ruta) or '.', exist_ok=True)
            
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(html)
            
            return True
        except Exception as e:
            print(f"Error al guardar factura: {e}")
            return False
    
    def intentar_generar_pdf(self, factura_id, ruta=None):
        """Intenta generar PDF (requiere reportlab)"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
            from reportlab.lib.units import inch
            
            factura = self.logica.obtener_factura(factura_id)
            if not factura:
                return False
            
            if ruta is None:
                ruta = f"Facturas/Factura_{factura['numero_factura']}.pdf"
            
            import os
            os.makedirs(os.path.dirname(ruta) or '.', exist_ok=True)
            
            # Crear documento
            doc = SimpleDocTemplate(ruta, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Título
            story.append(Paragraph("FACTURA ELECTRÓNICA", styles['Title']))
            story.append(Spacer(1, 0.3*inch))
            
            # Información básica
            info_text = f"""
            <b>Número:</b> {factura['numero_factura']}<br/>
            <b>Fecha:</b> {factura['fecha']}<br/>
            """
            story.append(Paragraph(info_text, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Items
            resumen = self.logica.generar_resumen_factura(factura_id)
            datos_tabla = [['Producto', 'Cantidad', 'Precio', 'Subtotal']]
            
            for item in resumen['items']:
                subtotal = item['cantidad'] * item['precio_unitario']
                datos_tabla.append([
                    item['nombre'],
                    str(item['cantidad']),
                    f"${item['precio_unitario']:.2f}",
                    f"${subtotal:.2f}"
                ])
            
            tabla = Table(datos_tabla)
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            story.append(tabla)
            story.append(Spacer(1, 0.3*inch))
            
            # Totales
            totales_text = f"""
            <b>Subtotal:</b> ${resumen['subtotal']:.2f}<br/>
            <b>IVA ({resumen['iva_porcentaje']}%):</b> ${resumen['iva_valor']:.2f}<br/>
            <b>TOTAL:</b> ${resumen['total']:.2f}
            """
            story.append(Paragraph(totales_text, styles['Normal']))
            
            doc.build(story)
            return True
            
        except ImportError:
            print("reportlab no está instalado. Usa: pip install reportlab")
            return False
        except Exception as e:
            print(f"Error al generar PDF: {e}")
            return False
