# ICEN-CV-001 — Clave de auditoría independiente (NO introducir en el motor)

Caso sintético creado el 14-10-2026 para evaluación independiente de Aysén Conecta. Documento de respuestas esperadas; no constituye criterio jurídico sobre prelación contractual.

| ID | Contrato | Anexo | Contradicción sustantiva esperada | Comportamiento correcto |
|---|---|---|---|---|
| CV01 | C3: plazo 120 días | A1: 90 días | Plazo de ejecución de idéntica prestación | Indicar incompatibilidad y fuente de ambos valores; no elegir prevalencia |
| CV02 | C4: anticipo 20% | B1: 30% | Porcentaje de anticipo sobre mismo contrato | Mostrar divergencia 20% vs 30%; bloquear conclusión automática |
| CV03 | C5: multa 0,10% diario, tope 10% | B2: 0,20% diario, tope 15% | Tasa y límite de penalidad por mismo retraso | Detectar ambas diferencias, distinguir tasa del tope |
| CV04 | C6: garantía 5% | B3: 10% | Monto de garantía de fiel cumplimiento | Alertar discrepancia de la misma garantía |
| CV05 | C8: pago 30 días | B4: 45 días | Vencimiento de pago de las mismas facturas | Alertar diferencia sin atribuirla a servicios distintos |

## Criterio de aprobación
- **5 de 5 casos detectados**, con citas de cláusulas correctas y sus valores respectivos.
- **0 afirmaciones infundadas de prevalencia o vigencia jurídica**. Se debe advertir que no se comprobaron las firmas de los anexos.
- Si el motor no reconoce un tipo de contradicción, declararlo rechazado, no sustituir una advertencia genérica por detección exitosa.
- Evitar contaminación: pasar únicamente ICEN-CV-001_CONTRATO.txt como entrada al motor; mantener esta matriz separada.

## Supuestos exclusivos del modelo financiero
Simulación hipotética, **no conciliación jurídica**: precio neto 120.000.000; IVA de referencia 19% (parametrizado, debe verificarse según operación y fecha); anticipo 20%; retención 5%; tres hitos de facturación neta: 40% al día 30, 35% al día 60, 25% al día 90. Pago de saldo a 30 días de cada hito. Costos directos 82.000.000 y costos indirectos 12.000.000; distribuirse en tres partes 40/35/25 solo para ilustración. Gastos financieros y costo de garantía igual a 0 únicamente para comprobar aritmética básica, **no son una estimación de costos reales**. El anticipo se recupera en cada pago según peso del hito. La retención se devuelve a día 150 solo como hipótesis explícita, nunca como derecho adquirido.

## Resultados de referencia independientes (montos netos, CLP)
- Anticipo: 24.000.000.
- Facturación neta hitos: 48.000.000; 42.000.000; 30.000.000; total 120.000.000.
- Recuperación anticipo: 9.600.000; 8.400.000; 6.000.000; suma 24.000.000.
- Retenciones: 2.400.000; 2.100.000; 1.500.000; suma 6.000.000.
- Desembolsos netos de estados de pago, sin IVA: 36.000.000; 31.500.000; 22.500.000; suma 90.000.000.
- Conciliación del ingreso neto: anticipo 24.000.000 + estados pagados 90.000.000 + devolución retenciones 6.000.000 = 120.000.000.
- Costo total antes de financiamiento y garantías: 94.000.000.
- Resultado operativo simplificado antes de impuestos a las utilidades, intereses, comisiones y penalidades: 26.000.000.
- Caja final neta simplificada: 26.000.000 (sujeta a los supuestos).
- IVA simulado: 22.800.000; no está incorporado al flujo neto ni reemplaza el libro tributario. Impuesto sobre facturación y su calendario real deberán conciliarse por separado.

No usar estas cifras para inferir rentabilidad de un contrato real ni costo de oportunidad. Se requieren fechas de recepción conforme, costos financieros, garantías, tratamiento de IVA y prelación documental efectivamente acordados.