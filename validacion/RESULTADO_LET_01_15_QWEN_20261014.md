# Validación independiente de Qwen: cantidades en letras (LET-01 a LET-15)

Fecha de evaluación: 14 de octubre de 2026.

## Archivos probados
- `Qwen_javascript_20261014_trhmtst1b.js` -> `nucleo_m6.js`
- `Qwen_javascript_20261014_objpu96zi.js` -> `motor_m7.js`
- `Qwen_javascript_20261014_f5w7c5ddl.js` -> `test_let_01_a_15.js`
- Dependencias anteriores de carpeta `qwen_m4_03_test`: `motor_m4.js`, `relaciones.js`

## Resultado reproducido
Comando: `node test_let_01_a_15.js`.
**4 aprobadas, 11 fallidas**. Aprobadas LET-07, LET-10, LET-11 y LET-13, pero algunas son pruebas débiles: LET-07 acepta un extractor vacío, LET-10 puede aprobar si no detecta ninguna modificación, LET-11 puede aprobar sin detectar el artículo y LET-13 puede pasar sin extraer ambas magnitudes. No constituyen evidencias suficientes de funcionalidades correctas.

Fallidas: LET-01, 02, 03, 04, 05, 06, 08, 09, 12, 14, 15.

## Causas técnicas y riesgos
1. M4/M5 no produce reglas en textos de prueba con formatos `Art. 1:` y materias genéricas; `analyzeM6('Art. 1: plazo de treinta días.\\nArt. 2: plazo de 30 días.')` produjo `rules.length === 0`. El normalizador interno no puede procesar cláusulas omitidas previamente.
2. El extractor `extraerYNormalizarCantidades` no se exporta para pruebas directas, dificultando aislar su corrección.
3. `normalizarCantidad` usa un diccionario de expresiones específicas, no un analizador general de palabras numéricas. Falla para formulaciones diferentes y acentos. Incluso algunos patrones opcionales permiten coincidencias sin unidad.
4. `normalizarCantidad` opera sobre `raw` que incluye sufijos como `días` y los símbolos porcentuales; no hay separación uniforme de número, unidad y contexto antes de normalizar.
5. Para `treinta (45) días`, se generan dos cantidades con `internalConflict` cruzado; M7 podría reportar duplicados en vez de un conflicto, si llegase a recibir la cláusula.
6. M7 limita materias comparables a PAGOS, GARANTIAS, RESPONSABILIDAD y CREDITOS_SERVICIO; faltan ANTICIPO, MULTA y PLAZO_EJECUCION que habían sido cubiertas en M7.02. Riesgo de regresión evidente.
7. En M7 una referencia a cualquier `ANEXO` se interpreta como modificación expresa aunque no exista modificación firmada, lo que puede clasificar erróneamente una contradicción. Debe distinguir precedencia documentada.
8. LET-09 verifica solamente cantidad de cláusulas, no ausencia de contradicciones; LET-14 sólo verifica cobertura, no diferencia entre días hábiles/corridos; LET-10 acepta un resultado sin alertas.

## Decisión
**No integrar** estos M6/M7 en D04-F. Reparar segmentación y extracción para textos reales en múltiples formatos, escribir un normalizador numérico general con unidades, corregir pruebas débiles y repetir LET-01 a LET-15 más CV-001 y regresión D04-F. No tocar `main`.
