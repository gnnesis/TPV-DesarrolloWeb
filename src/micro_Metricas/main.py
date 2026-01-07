from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

# Configurar la URL de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/tpv_relacional"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ============== MODELOS DE LA BD (SOLO LECTURA) ==============
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

# ============== SCHEMAS ==============
class MetricaVentaDiaria(BaseModel):
    fecha: date
    total_ventas: float
    numero_ventas: int
    promedio: float

class MetricaProducto(BaseModel):
    producto_id: str
    total_cantidad: int
    total_ingresos: float

# FastAPI app
app = FastAPI(title="Microservicio de Métricas (FastAPI)")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== DEPENDENCY ==============
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============== ENDPOINTS ==============

@app.get("/", tags=["status"])
def root():
    """Estado del microservicio"""
    return {
        "status": "ok",
        "service": "Microservicio de Métricas (FastAPI)",
        "version": "1.0.0"
    }

@app.get("/metricas/ventas-diarias", response_model=List[MetricaVentaDiaria], tags=["metricas"])
def get_ventas_diarias(db: Session = Depends(get_db)):
    """Obtener métricas de ventas por día"""
    resultados = db.query(
        VentaModel.fecha,
        func.sum(VentaModel.total).label('total_ventas'),
        func.count(VentaModel.id).label('numero_ventas')
    ).group_by(VentaModel.fecha).all()

    metricas = []
    for r in resultados:
        promedio = r.total_ventas / r.numero_ventas if r.numero_ventas > 0 else 0
        metricas.append(MetricaVentaDiaria(
            fecha=r.fecha,
            total_ventas=float(r.total_ventas),
            numero_ventas=r.numero_ventas,
            promedio=float(promedio)
        ))
    return metricas

@app.get("/metricas/resumen", tags=["metricas"])
def get_resumen_general(db: Session = Depends(get_db)):
    """Obtener resumen general de todas las ventas"""
    total_ventas = db.query(func.sum(VentaModel.total)).scalar() or 0
    numero_ventas = db.query(func.count(VentaModel.id)).scalar() or 0
    numero_mesas = db.query(func.count(VentaModel.mesa.distinct())).scalar() or 0
    promedio_venta = total_ventas / numero_ventas if numero_ventas > 0 else 0
    
    # Ventas de hoy
    hoy = date.today()
    ventas_hoy = db.query(func.sum(VentaModel.total)).filter(VentaModel.fecha == hoy).scalar() or 0
    
    # Total de productos vendidos (suma de cantidades en comandas)
    productos_vendidos = db.query(func.sum(ComandaModel.cantidad)).scalar() or 0

    return {
        "total_ingresos": float(total_ventas),
        "total_ventas": numero_ventas,
        "numero_mesas_usadas": numero_mesas,
        "promedio_venta": float(promedio_venta),
        "ventas_hoy": float(ventas_hoy),
        "productos_vendidos": productos_vendidos
    }

@app.get("/metricas/productos", response_model=List[MetricaProducto], tags=["metricas"])
def get_metricas_productos(db: Session = Depends(get_db)):
    """Obtener métricas por producto (requiere que el precio esté en comandas o productos)"""
    resultados = db.query(
        ComandaModel.producto_id,
        func.sum(ComandaModel.cantidad).label('total_cantidad')
    ).group_by(ComandaModel.producto_id).all()

    metricas = []
    for r in resultados:
        metricas.append(MetricaProducto(
            producto_id=r.producto_id,
            total_cantidad=r.total_cantidad,
            total_ingresos=0.0  # Se podría mejorar si tenemos tabla de precios
        ))
    return metricas

@app.get("/metricas/top-mesas", tags=["metricas"])
def get_top_mesas(db: Session = Depends(get_db), limite: int = 5):
    """Obtener las mesas con más ventas"""
    resultados = db.query(
        VentaModel.mesa,
        func.count(VentaModel.id).label('numero_ventas'),
        func.sum(VentaModel.total).label('total_ingresos')
    ).group_by(VentaModel.mesa).order_by(func.sum(VentaModel.total).desc()).limit(limite).all()

    mesas = []
    for r in resultados:
        mesas.append({
            "mesa": r.mesa,
            "numero_ventas": r.numero_ventas,
            "total_ingresos": float(r.total_ingresos)
        })
    return mesas

if __name__ == "__main__":
    import uvicorn
    print("\n✅ Microservicio de Métricas (FastAPI) iniciando...")
    print("📍 Documentación disponible en http://localhost:5003/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=5003)
