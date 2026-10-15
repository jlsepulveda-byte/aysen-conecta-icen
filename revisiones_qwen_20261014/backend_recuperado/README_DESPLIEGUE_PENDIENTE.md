# Revisión de infraestructura Qwen — propuesta no operativa

Se reconstruyeron Dockerfile, Compose, dependencias y migración desde el fragmento recibido.

- Compose tiene indentación válida, variables de entorno requeridas y PostgreSQL sin exposición de puerto al equipo anfitrión.
- El servidor HTTP queda enlazado a 127.0.0.1:8000 (solo equipo local).
- No se han ejecutado contenedores ni una instancia real PostgreSQL.
- El archivo SQL original proponía referencias legales no comprobadas: no se sembraron en esta versión de pruebas.
- Hay inconsistencia pendiente: se declaran los modelos Empresa, Documento y Norma, pero la migración crea únicamente Norma.
- Falta configuración de acceso a usuarios, políticas de seguridad multiempresa, migraciones completas y validación real.
- Las versiones de dependencias se conservan como referencia de Qwen; deben actualizarse y auditarse antes de producción.
- D04-F y main no se modifican.
