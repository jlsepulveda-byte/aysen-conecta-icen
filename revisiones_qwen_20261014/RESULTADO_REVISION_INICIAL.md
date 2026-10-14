# Inspección inicial de propuestas Qwen — 14-10-2026

**Estado:** propuestas recibidas, publicadas de forma separada, no integradas en D04-F.

## Verificación
- Script original: 555 líneas, **SyntaxError** por cadena triple sin cerrar en línea 550; por eso no genera el backend.
- Se recuperaron 12 archivos completos de propuestas y se publicaron como texto.
- Se ejecutó por separado el generador financiero recuperado: finalizó sin error y produjo un XLSX.
- Se examinaron sus celdas: B4 contiene `=C2-C3`, pero C4 contiene el valor fijo 26000000; B6/B7/B8 muestran fórmulas, pero C6/C7/C8 contienen valores fijos. Eso NO demuestra un libro financiero calculado dinámicamente.
- Su fórmula de conciliación B10 es `=SI(C6+C8+C7=C2, 'CONCILIACIÓN EXITOSA', 'ERROR DE CÁLCULO')`. Con sus valores: 24.000.000 + 114.000.000 + 6.000.000 = 144.000.000, no 120.000.000. La conciliación propuesta **NO CIERRA** y tiene doble conteo del anticipo. Además, la forma de cadenas con comillas simples no es una fórmula Excel confiable.
- El script no construye flujos de caja fechados ni amortización de anticipo por hitos, pese a anunciar estas prestaciones.
- El motor M7 v2 y la integración propuesta aún requieren pruebas sobre el caso contractual y las regresiones D04-C–D04-F.

## Decisión
Mantener material en `revisiones_qwen_20261014/` para auditoría; no fusionar ni sustituir motores de la aplicación. `main` intacta.

## Próximo criterio de aceptación
El Excel debe contener fórmulas funcionales en las celdas numéricas, una conciliación independiente con diferencia 0, movimientos fechados y amortización del anticipo por hitos; el motor M7 debe detectar cinco contradicciones precisas y evitar falsos positivos. Sólo integrar los cambios que superen pruebas reproducibles.
