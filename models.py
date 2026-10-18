from sqlalchemy import Column, Integer, String, DateTime
import enum
from datetime import datetime
from database import Base

class EstadoCita(str, enum.Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"

class CitaServicio(Base):
    __tablename__ = "citas_servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String, nullable=False)
    correo_cliente = Column(String, nullable=False)
    servicio = Column(String, nullable=False)
    fecha_cita = Column(String, nullable=False)
    estado = Column(String, default=EstadoCita.PENDIENTE.value)
    notas = Column(String, nullable=True)
    creado_el = Column(DateTime, default=datetime.utcnow)
