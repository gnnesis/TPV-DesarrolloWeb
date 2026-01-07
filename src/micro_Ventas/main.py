from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
import os

# Configurar la URL de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/tpv_relacional"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ============== MODELOS DE LA BD ==============
class ComandaModel(Base):
    __tablename__ = "comanda"
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("venta.id"), nullable=False)
    producto_id = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)

class VentaModel(Base):
    __tablename__ = "venta"
    id = Column(Integer, primary_key=True, index=True)
    mesa = Column(String(20), nullable=False)
    fecha = Column(Date, nullable=False, default=date.today)
    total = Column(Float, nullable=False)
    comandas = relationship("ComandaModel", backref="venta", cascade="all, delete-orphan")

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# ============== SCHEMAS PYDANTIC ==============
class Comanda(BaseModel):
    id: Optional[int] = None
    producto_id: str
    cantidad: int

    class Config:
        orm_mode = True

class VentaCreate(BaseModel):
    mesa: str
    total: float
    comandas: List[Comanda] = []

class VentaOut(BaseModel):
    id: int
    mesa: str
    fecha: date
    total: float
    comandas: List[Comanda] = []

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI(title="Microservicio de Ventas (FastAPI)")

# CORS (permitir peticiones desde el API Gateway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== DEPENDENCY: OBTENER SESIÓN DE BD ==============
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============== ENDPOINTS ==============

@app.get("/", tags=["status"])
def root():
    """Estado del microservicio y lista de endpoints"""
    return {
        "status": "ok",
        "service": "Microservicio de Ventas (FastAPI)",
        "version": "1.0.0"
    }

@app.get("/ventas", response_model=List[VentaOut], tags=["ventas"])
def get_ventas(db: Session = Depends(get_db)):
    """Obtener todas las ventas"""
    ventas = db.query(VentaModel).all()
    result = []
    for v in ventas:
        result.append(VentaOut(
            id=v.id,
            mesa=v.mesa,
            fecha=v.fecha,
            total=v.total,
            comandas=[Comanda(id=c.id, producto_id=c.producto_id, cantidad=c.cantidad) for c in v.comandas]
        ))
    return result

@app.get("/ventas/{venta_id}", response_model=VentaOut, tags=["ventas"])
def get_venta(venta_id: int, db: Session = Depends(get_db)):
    """Obtener una venta específica por ID"""
    v = db.query(VentaModel).filter(VentaModel.id == venta_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return VentaOut(
        id=v.id,
        mesa=v.mesa,
        fecha=v.fecha,
        total=v.total,
        comandas=[Comanda(id=c.id, producto_id=c.producto_id, cantidad=c.cantidad) for c in v.comandas]
    )

@app.post("/ventas", response_model=VentaOut, status_code=201, tags=["ventas"])
def create_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    """Crear una nueva venta con sus comandas"""
    v = VentaModel(mesa=venta.mesa, fecha=date.today(), total=venta.total)
    for c in venta.comandas:
        v.comandas.append(ComandaModel(producto_id=c.producto_id, cantidad=c.cantidad))
    db.add(v)
    db.commit()
    db.refresh(v)
    return VentaOut(
        id=v.id,
        mesa=v.mesa,
        fecha=v.fecha,
        total=v.total,
        comandas=[Comanda(id=c.id, producto_id=c.producto_id, cantidad=c.cantidad) for c in v.comandas]
    )

@app.get("/ventas/{venta_id}/comandas", response_model=List[Comanda], tags=["comandas"])
def get_comandas(venta_id: int, db: Session = Depends(get_db)):
    """Obtener todas las comandas de una venta"""
    v = db.query(VentaModel).filter(VentaModel.id == venta_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return [Comanda(id=c.id, producto_id=c.producto_id, cantidad=c.cantidad) for c in v.comandas]

@app.post("/ventas/{venta_id}/comandas", response_model=Comanda, status_code=201, tags=["comandas"])
def add_comanda(venta_id: int, comanda: Comanda, db: Session = Depends(get_db)):
    """Añadir una comanda a una venta existente"""
    v = db.query(VentaModel).filter(VentaModel.id == venta_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    c = ComandaModel(producto_id=comanda.producto_id, cantidad=comanda.cantidad, venta_id=venta_id)
    db.add(c)
    db.commit()
    db.refresh(c)
    return Comanda(id=c.id, producto_id=c.producto_id, cantidad=c.cantidad)

if __name__ == "__main__":
    import uvicorn
    print("\n✅ Microservicio de Ventas (FastAPI) iniciando...")
    print("📍 Documentación disponible en http://localhost:5001/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=5001)
