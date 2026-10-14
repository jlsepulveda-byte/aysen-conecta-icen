# Auditoría de afirmación Qwen — 14 octubre 2026

Revisión de archivos recibidos `Qwen_python_20261014_300so3gln.py` (553 líneas) y `Qwen_python_20261014_usf9c3yrv.py` (555 líneas).

## Prueba 1: compilación del generador
Comando: `python -m py_compile <archivo>` (equivalente de comprobación sintáctica con `ast.parse`).
Resultado: **RECHAZADA**. El primero termina con cadena de triple comilla abierta cerca de la línea 548; el segundo presenta el mismo defecto cerca de la línea 550. La afirmación «sin cortes» no es correcta para los archivos efectivamente recibidos.

## Prueba 2: conciliación financiera
Datos declarados: venta neta 120.000.000; anticipo 20%=24.000.000; facturación restante 96.000.000; retención del 5% sobre el restante=4.800.000; cobro=91.200.000; liberación=4.800.000.
Aritmética: `24.000.000+91.200.000+4.800.000=120.000.000`: **CORRECTA**, condicionado a que la retención se aplique al saldo facturado según contrato.
El código contiene fórmulas en C14, C15 y C16, pero las celdas de movimientos C7-C11 están fijadas como números: **no tiene un modelo dinámico completo**. C16 usa fórmula SI con comillas simples que puede ser inválida en motores de Excel; requiere corrección y prueba real del libro.

## Prueba 3: flujo fechado y amortización
No se identifican fechas, cronograma de desembolsos, amortizaciones por estado de pago ni cálculo del máximo déficit acumulado. **RECHAZADA** respecto de requisitos P0.

## Prueba 4: backend
Los fragmentos del servidor fueron reconstruidos como propuesta aislada en `revisiones_qwen_20261014/backend_recuperado/`, con parámetros seguros por defecto y sin despliegue. No se ha probado una instancia PostgreSQL, autenticación, autorización, migraciones ni el servicio completo. **NO VALIDADO**.

## Decisión
No modificar D04-F ni `main`; mantener propuestas separadas y no afirmar despliegue exitoso.
