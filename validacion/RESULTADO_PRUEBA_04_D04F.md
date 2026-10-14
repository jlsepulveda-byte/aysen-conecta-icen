# DOC-04 — Modificación expresa de plazo (D04-F) — 2026-10-14

**Resultado: APROBADO después de corrección.**

Caso:
- Contrato principal: pago de factura de suministro a 30 días corridos.
- Anexo: «Se modifica expresamente el plazo de pago de la factura de suministro y deberá realizarse dentro de 45 días corridos desde su recepción».

Resultados:
- Antes de corregir: no generaba alerta de modificación (0), **RECHAZADA**.
- Después de corregir: 1 `MODIFICACION_DOCUMENTAL_CANDIDATA`; 0 `CONTRADICCION_DOCUMENTAL_CANDIDATA`; cita ambos documentos, **APROBADA**.
- Regresión DOC-01, DOC-02 y DOC-03: las 3 aprobadas.
- 14 pruebas M7 aprobadas, 6 de generalización aprobadas.

Se actualizó `fuentes/motor_m7.js`, su código integrado en `fuentes/motor_m7_bundle.js` y el HTML de aplicación, y se añadió `pruebas/test_doc_04.js` al ZIP D04-F.

**Alcance**: sólo reconoce determinadas expresiones explícitas de modificación. No determina por sí mismo validez, jerarquía o cumplimiento de formalidades. Sin validación integral en navegador.

Archivo descargable entregado en la conversación: `AC-ICEN_2.8.0_D04F_CORRECCION_PRUEBA_04.zip`. No se modificó `main`.
