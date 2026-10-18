from sqlalchemy import Column, Integer, String, DateTime, Text
import enum
from datetime import datetime
from database import Base

class EstadoCita(str, enum.Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    FINALIZADO = "Finalizado"
    CANCELADA = "Cancelada"

class CitaServicio(Base):
    __tablename__ = "citas_servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String(100), nullable=False)
    correo_cliente = Column(String(100), nullable=False)
    servicio = Column(String(100), nullable=False)
    fecha_cita = Column(String(50), nullable=False)
    estado = Column(String(50), default=EstadoCita.PENDIENTE.value, nullable=False)
    notas = Column(Text, nullable=True)
    creado_el = Column(DateTime, default=datetime.utcnow)
