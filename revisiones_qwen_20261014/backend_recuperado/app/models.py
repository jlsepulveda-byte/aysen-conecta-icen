from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from .database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    rut = Column(String(12), unique=True, index=True, nullable=False)
    razon_social = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    region = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class Norma(Base):
    __tablename__ = "normas"
    id = Column(String(50), primary_key=True)
    materia = Column(String(100), nullable=False, index=True)
    norma = Column(String(255), nullable=False)
    articulo = Column(String(100), nullable=False)
    resumen = Column(Text, nullable=False)
    fuente = Column(String(500), nullable=False)
    fecha_consulta = Column(String(10), nullable=False)
    estado = Column(String(50), nullable=False)

class Documento(Base):
    __tablename__ = "documentos"
    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False, index=True)
    nombre_archivo = Column(String(255), nullable=False)
    sha256 = Column(String(64), index=True, nullable=False)
    tipo = Column(String(20), nullable=False)
    tamano = Column(Integer)
    ruta_almacenamiento = Column(String(500), nullable=False)
    metadata_json = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
