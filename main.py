from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqladmin import Admin, ModelView
from pydantic import BaseModel
from typing import List, Optional

import models
from database import engine, get_db

# Crear tablas automáticas en SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Agendamiento de Servicios TI - Parcial Híbrido",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de SQLAdmin (Panel Visual)
admin = Admin(app, engine, title="Panel de Administración - Servicios TI")

class CitaServicioAdmin(ModelView, model=models.CitaServicio):
    column_list = [
        models.CitaServicio.id,
        models.CitaServicio.nombre_cliente,
        models.CitaServicio.servicio,
        models.CitaServicio.fecha_cita,
        models.CitaServicio.estado,
        models.CitaServicio.creado_el,
    ]
    column_searchable_list = [models.CitaServicio.nombre_cliente, models.CitaServicio.servicio]
    column_filters = [models.CitaServicio.estado, models.CitaServicio.servicio]
    name = "Cita de Servicio"
    name_plural = "Citas de Servicios TI"
    icon = "fa-solid fa-calendar-check"

admin.add_view(CitaServicioAdmin)

# Schemas de Pydantic
class CitaCreate(BaseModel):
    nombre_cliente: str
    correo_cliente: str
    servicio: str
    fecha_cita: str
    notas: Optional[str] = None

class CitaResponse(CitaCreate):
    id: int
    estado: str

    class Config:
        from_attributes = True

# Endpoints
@app.get("/")
def root():
    return {
        "mensaje": "API de Agendamiento de Servicios TI Activa",
        "panel_admin": "/admin",
        "documentacion": "/docs"
    }

@app.get("/citas", response_model=List[CitaResponse])
def listar_citas(db: Session = Depends(get_db)):
    return db.query(models.CitaServicio).all()

@app.post("/citas", response_model=CitaResponse)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    nueva_cita = models.CitaServicio(**cita.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita
