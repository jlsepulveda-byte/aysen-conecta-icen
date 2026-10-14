# Propuestas Qwen · AC-ICEN D04-C

Este directorio contiene todas las correcciones y mejoras propuestas para la migración a D04-C, respetando la base canónica 2.7.0.

## Estructura
- `correccion_p0_cv001/`: Correcciones 1-6 del caso de validación financiera ICEN-CV-001.
- `motor_m7_v2/`: Motor M7 mejorado con detección de prelaciones, extracción numérica con contexto y niveles de confianza.
- `integracion_m7_calculadora_v2/`: Transferencia asistida M7 → Calculadora con confirmación humana obligatoria.
- `asistente_primer_uso/`: Micro-tours contextuales para reducir la fricción de UX en no especialistas.
- `backend_d04c/`: Migración a web centralizada (FastAPI + PostgreSQL + Docker).

## Próximos pasos
1. Revisar los archivos generados.
2. Ejecutar las pruebas unitarias de cada módulo.
3. `git add propuestas_qwen/`
4. `git commit -m "propuestas: paquete completo D04-C, M7 v2, asistente UX, CV-001"`
