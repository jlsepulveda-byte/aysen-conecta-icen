"""Generador reproducible del Excel de ICEN-CV-001. Requiere artifact_tool."""
from pathlib import Path
from datetime import datetime
from decimal import Decimal
from artifact_tool import Workbook, SpreadsheetFile

OUTPUT=Path(__file__).with_name('ICEN-CV-001_FLUJO_Y_CONCILIACION.xlsx')
w=Workbook.create()
s=w.worksheets.add('Supuestos')
s.get_range('A1:C11').values=[
 ['ICEN-CV-001 — SUPUESTOS SINTETICOS','Valor','Observación'],
 ['Precio neto',120000000,'C2'],['Anticipo %',0.20,'C4; contradicción B1'],
 ['Retención %',0.05,'C7'],['IVA ilustrativo %',0.19,'No mezclado con caja neta'],
 ['Costos directos',82000000,'C9'],['Costos indirectos',12000000,'C9'],
 ['Costo financiero',0,'Solo prueba aritmética'],['Costo garantía',0,'Solo prueba aritmética'],
 ['Fecha inicio',datetime(2026,11,1),'Hipótesis'],['Plazo pago (días)',30,'C8; contradicción B4']]
s.get_range('B10').set_number_format('yyyy-mm-dd')
p=w.worksheets.add('Estados de pago')
p.get_range('A1:K1').values=[['Hito','Fracción','Día hito','Fecha factura','Base neta','Anticipo recuperado','Retención','Pago neto','Fecha cobro','Costos asociados','Caja del hito']]
for row,(fraction,day) in enumerate([(0.40,30),(0.35,60),(0.25,90)],2):
 p.get_range(f'A{row}:C{row}').values=[[row-1,fraction,day]]
 f={'D':f'=Supuestos!$B$10+C{row}','E':f'=Supuestos!$B$2*B{row}',
    'F':f'=E{row}*Supuestos!$B$3','G':f'=E{row}*Supuestos!$B$4',
    'H':f'=E{row}-F{row}-G{row}','I':f'=D{row}+Supuestos!$B$11',
    'J':f'=(Supuestos!$B$6+Supuestos!$B$7)*B{row}','K':f'=H{row}-J{row}'}
 for col,formula in f.items():p.get_range(f'{col}{row}').formulas=[[formula]]
 for col in ['D','I']:p.get_range(f'{col}{row}').set_number_format('yyyy-mm-dd')
p.get_range('A5').values=[['TOTAL']]
for col in ['B','E','F','G','H','J','K']:p.get_range(f'{col}5').formulas=[[f'=SUM({col}2:{col}4)']]
c=w.worksheets.add('Conciliacion')
c.get_range('A1:C14').values=[
 ['Concepto','Monto o prueba','Explicación'],
 ['Precio neto',None,'Contrato'],['Anticipo recibido',None,'Antes del inicio'],
 ['Cobros por estados',None,'Después de descuentos'],
 ['Retenciones liberadas',None,'Hipótesis día 150'],
 ['Total ingreso conciliado',None,'Debe igualar precio neto'],
 ['Diferencia conciliación',None,'Debe ser cero'],
 ['Anticipo recuperado',None,'Debe igualar anticipo'],
 ['Diferencia anticipo',None,'Debe ser cero'],
 ['Retención acumulada',None,'Debe igualar devolución'],
 ['Diferencia retención',None,'Debe ser cero'],
 ['Costos totales',None,'Incluye gastos financiados hipotéticos'],
 ['Resultado simplificado',None,'No equivale a utilidad neta tributaria'],
 ['IVA ilustrativo',None,'Fuera del flujo neto']]
formulas={2:'=Supuestos!B2',3:'=Supuestos!B2*Supuestos!B3',
 4:"='Estados de pago'!H5",5:"='Estados de pago'!G5",
 6:'=SUM(B3:B5)',7:'=B6-B2',8:"='Estados de pago'!F5",
 9:'=B8-B3',10:"='Estados de pago'!G5",
 11:'=B10-B5',12:'=SUM(Supuestos!B6:B9)',
 13:'=B6-B12',14:'=B2*Supuestos!B5'}
for row,formula in formulas.items():c.get_range(f'B{row}').formulas=[[formula]]
for sh in [s,p,c]:
 sh.get_range('A1:K1').format.row_height=30
 sh.get_range('A:A').format.column_width=26
 sh.get_range('B:B').format.column_width=21
 sh.get_range('C:C').format.column_width=48 if sh!=p else 14
 if sh==p:sh.get_range('D:K').format.column_width=22
SpreadsheetFile.export_xlsx(w).save(str(OUTPUT))
print('GENERADO',OUTPUT)
price=Decimal(120_000_000); fractions=[Decimal('.40'),Decimal('.35'),Decimal('.25')]
advance=price*Decimal('.20')
holdback=price*Decimal('.05')
recover=sum((price*f*Decimal('.20') for f in fractions),Decimal(0))
retain=sum((price*f*Decimal('.05') for f in fractions),Decimal(0))
paid=sum((price*f*Decimal('.75') for f in fractions),Decimal(0))
assert advance==recover==Decimal(24_000_000)
assert holdback==retain==Decimal(6_000_000)
assert paid==Decimal(90_000_000)
assert advance+paid+retain==price
assert price-Decimal(82_000_000)-Decimal(12_000_000)==Decimal(26_000_000)
print('ORACULOS_ARITMETICOS_OK; NO ES VALIDACION DEL MOTOR M7 NI AUDITORIA TRIBUTARIA')
