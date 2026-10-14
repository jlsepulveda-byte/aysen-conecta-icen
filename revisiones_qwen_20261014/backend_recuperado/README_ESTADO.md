# Backend Qwen recuperado de fragmentos — NO VALIDADO PARA PRODUCCIÓN

Origen: fragmentos proporcionados en la conversación el 14-10-2026.
Los archivos originales de Qwen contenían saltos de línea perdidos, identificadores inválidos y valores de ejemplo inseguros. Estos cinco archivos se reconstruyeron con sintaxis Python válida de manera aislada y NO sustituyen la aplicación D04-F.

Diferencias deliberadas de seguridad: credenciales obligatorias a través de variables de entorno (sin valores por defecto), sin CORS abierto, sin creación automática de tablas durante importación, sin publicación automática de documentos, sin asegurar vigencia jurídica. La conectividad real con PostgreSQL y la autenticación aún NO han sido verificadas. El servicio no es completo.

Condiciones pendientes: migraciones consistentes con modelos, pruebas de API y base, autorización multiempresa, validación de archivos, secretos, manejo de errores y configuración segura de despliegue.
