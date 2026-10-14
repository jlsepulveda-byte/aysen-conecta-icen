# Prueba DOC-03 — resultado ejecutado (D04-E, 14-10-2026)

Caso: la factura de **suministro de equipos** vence en 30 días; la factura por **entrega de equipos** vence en 45 días. El sistema debe levantar una contradicción candidata, ya que ambas cláusulas se refieren expresamente al mismo bien.

- D04-D, antes de corregir: **0 alertas**, prueba **rechazada** (falso negativo).
- D04-E, después de corregir: **1 alerta**, prueba **aprobada**.
- Regresión DOC-01, mismo objeto: 1 alerta — **aprobada**.
- Regresión DOC-02, objetos distintos (suministro y mantención): 0 alertas — **aprobada**.
- Motor M7: 14 pruebas aprobadas.
- Generalización: 6 pruebas aprobadas.
- Comprobaciones D04-B: 13 aprobadas y 55 pantallas conservadas.

Se modificaron `fuentes/motor_m7.js`, `fuentes/motor_m7_bundle.js` y el HTML de aplicación, y se agregó `pruebas/test_doc_03.js`. La equivalencia es limitada a suministro/entrega de equipos, maquinarias o materiales. No demuestra comprensión semántica general ni validez jurídica.

El paquete D04-E actualizado se entregó como ZIP en la conversación. Esta rama solo registra el resultado, no contiene aún el código desplegado íntegramente. `main` no ha sido modificada.
