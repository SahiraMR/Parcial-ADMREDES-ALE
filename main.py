from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from sqlalchemy.orm import Session
from sqladmin import Admin, ModelView
from pydantic import BaseModel
from typing import List, Optional

import models
from database import engine, get_db

# Crear tablas automáticas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Agendamiento de Servicios TI - Parcial Híbrido",
    version="1.0.0"
)

# Acepta y procesa las cabeceras X-Forwarded-* que envía Apache
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Configuración de CORS permisiva
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de SQLAdmin (Panel Visual)
admin = Admin(app, engine, title="Panel de Administración - Servicios TI", base_url="/admin")

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
    
    name = "Cita de Servicio"
    name_plural = "Citas de Servicios TI"
    icon = "fa-solid fa-calendar-check"

admin.add_view(CitaServicioAdmin)

# Schemas de Pydantic para la respuesta de la API y documentación
class CitaResponse(BaseModel):
    id: int
    nombre_cliente: str
    correo_cliente: str
    servicio: str
    fecha_cita: str
    notas: Optional[str] = None
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
def crear_cita(
    nombre_cliente: str = Form(...),
    correo_cliente: str = Form(...),
    servicio: str = Form(...),
    fecha_cita: str = Form(...),
    notas: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    cita_data = {
        "nombre_cliente": nombre_cliente,
        "correo_cliente": correo_cliente,
        "servicio": servicio,
        "fecha_cita": fecha_cita,
        "notas": notas
    }
    nueva_cita = models.CitaServicio(**cita_data)
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita
