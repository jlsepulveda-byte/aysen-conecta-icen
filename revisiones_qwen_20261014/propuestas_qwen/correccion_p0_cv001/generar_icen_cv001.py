import openpyxl
from decimal import Decimal, ROUND_HALF_UP

def generar_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Conciliacion_Financiera"
    
    # Parámetros
    VENTA_NETA = Decimal('120000000')
    COSTO_TOTAL = Decimal('94000000')
    PORC_ANTICIPO = Decimal('0.20')
    PORC_RETENCION = Decimal('0.05')
    
    # Cálculos
    anticipo = VENTA_NETA * PORC_ANTICIPO
    retencion_total = VENTA_NETA * PORC_RETENCION
    cobro_efectivo = VENTA_NETA - retencion_total
    
    # Escritura en celdas con fórmulas
    ws['A1'] = "CONCEPTO"
    ws['B1'] = "FÓRMULA / VALOR"
    ws['C1'] = "MONTO (CLP)"
    
    ws['A2'], ws['B2'], ws['C2'] = "Venta Neta", "Dato base", float(VENTA_NETA)
    ws['A3'], ws['B3'], ws['C3'] = "Costo Total", "Dato base", float(COSTO_TOTAL)
    ws['A4'], ws['B4'], ws['C4'] = "Margen Bruto", "=C2-C3", None
    ws['C4'] = float(VENTA_NETA - COSTO_TOTAL)
    
    ws['A6'], ws['B6'], ws['C6'] = "Anticipo (20%)", "=C2*0.20", float(anticipo)
    ws['A7'], ws['B7'], ws['C7'] = "Retención Total (5%)", "=C2*0.05", float(retencion_total)
    ws['A8'], ws['B8'], ws['C8'] = "Cobro Efectivo Neto", "=C2-C7", float(cobro_efectivo)
    
    # Validación de conciliación
    ws['A10'] = "VALIDACIÓN DE CONCILIACIÓN"
    ws['B10'] = "=SI(C6+C8+C7=C2, 'CONCILIACIÓN EXITOSA', 'ERROR DE CÁLCULO')"
    
    wb.save("ICEN_CV001_MODELO_FINANCIERO.xlsx")
    print("✅ Excel generado con fórmulas reales en ICEN_CV001_MODELO_FINANCIERO.xlsx")

if __name__ == "__main__":
    generar_excel()
