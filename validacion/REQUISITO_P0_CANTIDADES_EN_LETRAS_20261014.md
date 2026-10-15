# Requisito P0 — cantidades expresadas en letras y cifras

**Origen:** observación del usuario, 14-10-2026. **Estado:** criterio de aceptación propuesto, NO implementación aprobada.

## Alcance obligatorio M4 → M6 → M7
- Reconocer cantidades en letras: cero, diez, veinte, treinta, cuarenta y cinco, noventa, ciento veinte, doscientos ochenta y cinco; miles y millones.
- Reconocer cifras numéricas: `30`, `0,10%`, `$2.500.000`, `CLP 24.000.000`.
- Contextualizar unidad y materia: días hábiles/corridos, meses, CLP, porcentajes, tasas diarias, tope, garantía, retención, anticipo, monto por hito.
- Asociar valores al concepto correcto y preservar cita literal, cláusula, documento y página.
- Evitar duplicados cuando cifra y palabra describen el mismo valor.
- Detectar incongruencias *dentro* de la misma cláusula (ej. `treinta (45) días`) y entre contrato/anexo.
- No interpretar numerales romanos de artículos como montos económicos.
- No confundir `un millón doscientos mil` con `un millón doscientos`, ni `cero coma diez por ciento` con `diez por ciento`.
- Prestar atención a plural, género, tildes, conectores, abreviaturas y separadores chilenos.

## Casos de prueba obligatorios
| ID | Cláusula o comparación | Esperado |
|---|---|---|
| LET-01 | Treinta días vs 30 días | equivalencia, sin alerta |
| LET-02 | Treinta días vs cuarenta y cinco días | contradicción si es misma obligación |
| LET-03 | Ciento veinte días vs 90 días | contradicción mismo objeto |
| LET-04 | Veinte por ciento vs 20% | equivalencia, sin alerta |
| LET-05 | Cero coma diez por ciento vs 0,20% | contradicción misma tasa |
| LET-06 | Dos millones quinientos mil pesos vs $2.500.000 | equivalencia |
| LET-07 | Treinta (30) días | un solo valor normalizado |
| LET-08 | Treinta (45) días | discrepancia interna y bloqueo |
| LET-09 | Plazo entrega suministro 30 días; mantenimiento 45 días | no contradicción por objetos distintos |
| LET-10 | Anexo firmado modifica expresamente 30 días por 45 días | modificación, no contradicción simple |
| LET-11 | Artículo IV y Cláusula C3 | numeración estructural, no importe |
| LET-12 | Un millón doscientos mil pesos vs $1.200.000 | equivalencia |
| LET-13 | 0,10 % diario, tope diez por ciento | tasa y tope distintos, no enfrentarlos entre sí |
| LET-14 | Diez días hábiles vs diez días corridos | diferencia de unidad/cómputo, advertencia |
| LET-15 | Noventa y cinco mil pesos vs $95.000 | equivalencia |

## Criterio de aceptación
Cada caso debe devolver valores normalizados, evidencia completa, objeto comparado, alerta sólo cuando corresponde y confirmación humana para conflictos. Agregar casos negativos y pruebas de regresión D04-C a D04-F. No se autoriza alterar `main` ni el motor vigente hasta validar.

**Riesgo detectado:** los extractores numéricos actuales trabajan sobre regex de cifras; las cantidades escritas en letras no aparecen como valores numéricos normalizados. Es una brecha que requiere desarrollo, no sólo actualización documental.
