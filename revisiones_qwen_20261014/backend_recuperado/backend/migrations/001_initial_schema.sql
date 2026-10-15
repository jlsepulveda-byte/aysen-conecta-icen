-- Esquema de demostración; compatibilidad con modelos y migraciones futuras pendiente.
CREATE TABLE IF NOT EXISTS normas (
  id VARCHAR(50) PRIMARY KEY,
  materia VARCHAR(100) NOT NULL,
  norma VARCHAR(255) NOT NULL,
  articulo VARCHAR(100) NOT NULL,
  resumen TEXT NOT NULL,
  fuente VARCHAR(500) NOT NULL,
  fecha_consulta VARCHAR(10) NOT NULL,
  estado VARCHAR(50) NOT NULL
);
-- No se insertan referencias jurídicas no verificadas como si estuviesen validadas.
