# Plan verificable de validación integral — AC-ICEN 2.8.0 D04-B

Fecha: 2026-10-14
Estado: PLAN DE PRUEBAS, NO CERTIFICACIÓN.
Rama de trabajo: `validacion-integral-d04c-c01f-20261014`
Fuente inicial: `AC-ICEN_2.8.0_D04B_CONSULTA_AUTOMATICA_20261013 (6).zip`

## Condiciones previas y control de versiones
- No modificar ni fusionar directamente la rama principal `main`.
- Descomprimir el paquete de código y publicar los archivos fuente legibles en esta rama, eliminando cualquier credencial y evitando datos personales reales.
- Registrar versión exacta, hash de entrada, dependencias, comandos de ejecución y datos de prueba sintéticos.
- Las pruebas deben fallar de modo visible, con resultados reproducibles y evidencia; no sustituir resultados con apreciaciones.
- Ninguna recomendación de la plataforma deberá presentarse como certeza legal, comercial o financiera sin fundamento verificable.

## Matriz inicial de casos críticos

| Código | Módulo | Escenario / oráculo | Resultado |
|---|---|---|---|
| CAL-01 | Calculadora | Anticipo: monto pagado inicialmente se descuenta una sola vez del saldo; el total no se duplica | Pendiente |
| CAL-02 | Calculadora | Multa diaria con tope: aplicar base, días y límite según cláusula indicada, sin superar el tope | Pendiente |
| CAL-03 | Calculadora | IVA: distinguir precio neto, impuesto y precio bruto; no presumir si el contrato no indica tratamiento | Pendiente |
| CAL-04 | Calculadora | Margen vs recargo: distinguir utilidad/precio de venta de utilidad/costo; mostrar fórmulas | Pendiente |
| CAL-05 | Calculadora | Costos indirectos, garantías, retenciones y costo financiero: trazabilidad y no doble conteo | Pendiente |
| CAL-06 | Calculadora | Monto cero, cifras negativas, campos vacíos y números inválidos: mensaje explicativo; sin resultado ficticio | Pendiente |
| DOC-01 | Análisis documental | Extraer partes, montos, plazos, hitos, multas y garantías con cláusula/página fuente | Pendiente |
| DOC-02 | Análisis documental | Cláusula ausente o ambigua: declarar «No determinado»; no inventar datos | Pendiente |
| DOC-03 | Análisis documental | Contradicciones entre anexos y contrato: marcar conflicto sin decidir silenciosamente | Pendiente |
| DOC-04 | Análisis documental | Documento escaneado ilegible: advertencia explícita; evitar falsa certeza | Pendiente |
| INT-01 | Integración | Importar montos/plazos extraídos al cálculo con confirmación y trazabilidad | Pendiente |
| INT-02 | Integración | Cambio del documento o de una cláusula invalida cálculos anteriores relacionados | Pendiente |
| SEG-01 | Seguridad | Archivos de terceros, instrucciones incrustadas y contenido malicioso no alteran reglas del sistema | Pendiente |
| SEG-02 | Seguridad | Acceso entre usuarios/empresas, permisos y eliminación segura de datos | Pendiente |
| REG-01 | Regresión | Conjunto de contratos sintéticos: mismos insumos producen mismos resultados versionados | Pendiente |

## Contrato sintético para prueba simultánea
- Precio neto de servicio: $120.000.000.
- Anticipo contractual: 20% del precio neto, recuperado proporcionalmente en estados de pago.
- Plazo de ejecución: 120 días corridos.
- Multa por atraso imputable: 0,1% del precio neto por día, máximo 10% del precio neto.
- Garantía de fiel cumplimiento: 5% del precio neto (instrumento y costo por determinar).
- Retención de cada estado de pago: 5% hasta un máximo acumulado del 5% del precio neto, con devolución condicionada a recepción conforme.
- Costos directos declarados: $82.000.000; costos indirectos: $12.000.000; costo del financiamiento: a ingresar por el analista.
- Anexo contradictorio: sostiene plazo de 90 días. El analizador debe detectar contradicción, no elegir silenciosamente.
- El tratamiento del IVA y la prevalencia de anexos requieren texto contractual; no se deben asumir.

Este contrato es FICTICIO y sus valores solo sirven para comprobar la lógica del sistema; no constituyen precios de mercado ni asesoría jurídica.

## Criterios de aceptación
1. Cada cálculo presenta insumos, fórmulas, desglose, fuente documental y advertencias aplicables.
2. El analizador entrega referencias rastreables al texto contractual y clasifica incertidumbre de forma explícita.
3. En discrepancias críticas entre contrato y anexos, se bloquea la conclusión automática hasta revisión.
4. Pruebas unitarias, integración y regresión se ejecutan y registran con comandos, fecha, versión y resultados.
5. Solo promover cambios hacia `main` tras revisión humana y comprobación de controles; no realizar fusión automática.

## Hallazgos de inspección inicial
- En la raíz del repositorio solo aparecen un README y un archivo ZIP de 1.464.210 bytes.
- La existencia de código ejecutable, pruebas, dependencias y condiciones de despliegue **todavía no está verificada**, pues el paquete ZIP no se ha podido inspeccionar en esta sesión.
- La rama `main` aparece como `protected: false`. Trabajar exclusivamente en la rama de validación reduce riesgo de cambios accidentales, pero NO equivale a configurar reglas de protección en GitHub.
