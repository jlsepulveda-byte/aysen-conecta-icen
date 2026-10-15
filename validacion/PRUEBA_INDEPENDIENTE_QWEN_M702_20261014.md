# Revalidación independiente Qwen M7.02 — 14-10-2026

## Material
- `Qwen_javascript_20261014_t6mfbk6zm.js`: motor M7.02 recibido.
- `Qwen_javascript_20261014_bcvzdae68.js`: prueba `test_cv001.js` recibida.
- `Qwen__20261014_p7yb1r6sm.txt`: salida que Qwen informa (9/9).
- Dependencias reales extraídas del paquete D04-F: `nucleo_m6.js`, `motor_m4.js`, `relaciones.js`.

## Ejecución independiente
Comando: `node test_cv001.js` (motor renombrado `motor_m7_v2.js`, dependencias disponibles).
- Resultado: **6 aprobadas, 3 fallidas**.
- Detectadas realmente: **2 contradicciones**: `PAGOS 30 vs 45`, `GARANTIAS 5 vs 10`.
- No detectadas: `PLAZO_EJECUCION 120 vs 90`, `ANTICIPO 20 vs 30`, `MULTA 0,10% vs 0,20%`.
- Pruebas de seguridad: revisión humana, confianza BLOQUEADA, sin conclusión jurídica y sin exportación financiera automática: **4 aprobadas**.

## Causa observada
Ejecutando `analyzeM6` directamente con el contrato simplificado de la prueba se generan **5 reglas candidatas**: C6, C7, C8, B3 y B4. No produce reglas para C3, A1, C4, B1, C5 ni B2. M7 depende de `base.rules` y no puede comparar cláusulas que no llegaron a la extracción. El parche de normalización de sección ocurre después de ese filtro, por lo que no soluciona el problema.

## Control de regresión
`node test_m7_baseline.js` con el contrato maestro extraído y archivos del paquete D04-F: **14 pruebas aprobadas**.

## Decisión
**No integrar M7.02** todavía: su afirmación de 9/9 no se reproduce con el conjunto de dependencias vigente. Conservarlo como propuesta; reparar extracción en M4/M6 y probar falsos positivos en excepciones/anexos antes de considerar fusión. No modificar `main` ni código operativo D04-F.

### Alcance
La prueba compara Qwen M7.02 con el M4/M6 incluido en el ZIP D04-F; no se conoce el entorno exacto con el que Qwen obtuvo 9/9. Ese resultado podría depender de una versión distinta del segmentador o de otras dependencias no adjuntas.
