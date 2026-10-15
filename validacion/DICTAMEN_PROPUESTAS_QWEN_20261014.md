# Evaluación ejecutada de propuestas Qwen — 14 octubre 2026

**Base comparada:** paquete local AC-ICEN 2.8.0 D04-F; se descomprimió en entorno aislado, sin modificar el original. **Fuentes Qwen:** archivos Python adjuntos, recuperando 12 componentes cerrados del generador que llegó truncado.

## Pruebas ejecutadas
1. Generadores Qwen de 553 y 555 líneas: análisis sintáctico Python **FALLA** por cadena triple sin cerrar, en torno a líneas 548 y 550. Se recuperaron 12 contenidos completos por archivo sin ejecutar el generador truncado.
2. JavaScript Qwen M7 v2, integrador y asistente: `node --check` sin error de sintaxis. Esto **NO** constituye prueba funcional.
3. M7 v2: para funcionar requirió dependencias del código existente: `nucleo_m6.js`, `relaciones.js` y `motor_m4.js`. Invocación real `analyzeM7({documents:[{id:'cv001',text:contratoQwen}]})`: **5 cláusulas candidatas, 2 contradicciones**: pagos 30 vs 45 días y garantía 5% vs 10%. **FALLA** criterio de 5 contradicciones sustantivas. No reemplazar motor D04-F.
4. Pruebas heredadas D04-F: `node fuentes/test_m7.js` -> **14 pruebas aprobadas** en su propia suite; no implica que todo D04-F haya sido probado end-to-end.
5. Asistente de Qwen: 4 destinos o campos (`c_sale`, `c_pay`, `m7Out`, `m7Guard`) localizados en el HTML D04-F; destino `inicio` como ID no localizado. Se corrigió referencia inicial y el error de doble navegación ante excepción. Versión candidata `validacion/ASISTENTE_QWEN_CANDIDATO_20261014.js` con sintaxis comprobada. **Aún no integrado en HTML ni probado en navegador**, por lo que no se considera aprobado ni activo.
6. Calculadora: Qwen rectificó una conciliación básica: 24M + 91,2M + 4,8M = 120M. Sin embargo, fórmula dinámica sólo en celdas finales, cifras principales fijadas en código; no hay amortización por hitos ni flujos fechados. **FALLA** los criterios P0. Además, contrato prescribe retención 5% de cada estado de pago, sin establecer explícitamente que debe aplicarse sólo a neto post-anticipo.
7. Integración M7->Calculadora: se revisó código y sintaxis, pero no existe un circuito probado de la interfaz; no integrar. Puntos a corregir: unidades de plazo (días vs meses), bloqueo de sugerencias cuando confianza BLOQUEADA y manejo de eventos/cambio de valor.
8. Backend: infraestructura aislada en `revisiones_qwen_20261014/backend_recuperado`; no se ha levantado servidor ni base, y la migración no define todas las tablas de los modelos. **NO APTO** para fusión.

## Decisiones
- **Aprobar sólo como candidato experimental**, no como función ya instalada: asistente de primer uso en dos niveles. Publicado código candidato.
- **Rechazar para integración** M7 v2 y motor financiero Qwen en su estado actual; seguir mejoras por pruebas y correcciones.
- **Aplazar** integración M7-calculadora y migración FastAPI/PostgreSQL.
- **Mantener** D04-F como referencia; `main` intacta. Ningún cambio funcional se ha fusionado en la app.

## Próxima aceptación concreta
Para adoptar el asistente: ejecutar recorrido real en navegador y probar cerrar, volver a abrir, niveles Ejecutivo/Detallado, interrupciones de navegación, persistencia y ausencia de pérdida de datos. Para M7: casos positivos CV01-CV05 y negativos de anexos válidos, sin falsos positivos. Para finanzas: Excel dinámico con calendario y reconciliaciones comprobadas.
