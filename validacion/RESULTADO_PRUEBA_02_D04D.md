# Prueba DOC-02 — 14 octubre 2026

Escenario: contrato exige pago de factura de suministro en 30 días corridos; anexo exige pago de factura por mantención en 45 días corridos.

Resultado inicial D04-C: RECHAZADA — alerta incorrecta de contradicción.
Corrección D04-D: extracción conservadora del objeto expresamente identificado en la factura; cuando ambos objetos son distintos, el motor no declara contradicción por la sola diferencia de plazo.

Verificación ejecutada:
- DOC-02: 0 alertas de contradicción — APROBADA.
- DOC-01 (mismo objeto, 30 vs 45 días): 1 contradicción documental candidata — APROBADA.
- 14 pruebas de M7 — APROBADAS.
- 6 pruebas de generalización — APROBADAS.

Limitación importante: esta regla es heurística; los objetos implícitos o expresados de forma diferente pueden requerir revisión humana. No se ha ejecutado navegación integral.
Archivo de entrega local: AC-ICEN_2.8.0_D04D_CORRECCION_PRUEBA_02.zip. La rama principal no se modifica.
