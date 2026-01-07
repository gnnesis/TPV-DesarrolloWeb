# TPV - Sistema de Punto de Venta (FastAPI + Express + Node.js)

Sistema de Punto de Venta basado en microservicios para gestión de ventas, productos y analíticas. **Usando FastAPI y Express**.

---

## Arquitectura

| Componente | Tecnología | Puerto |
|---|---|---|
| **API Gateway** | Node.js + Express | 8080 |
| **Microservicio Ventas** | FastAPI (Python) | 5001 |
| **Microservicio Productos** | Node.js + Express | 5002 |
| **Microservicio Métricas** | FastAPI (Python) | 5003 |
| **Base de datos relacional** | MySQL | 3306 |
| **Base de datos no relacional** | MongoDB | 27017 |

---

## Software Necesario

1. **Python 3.10+**
2. **Node.js v16+**
3. **MySQL Server**
4. **MongoDB**

Verifica las instalaciones:
```bash
python --version
node --version
mysql --version
mongod --version
```

---

## 📂 Estructura del Proyecto

```
src/
├── apiGateway/         # API Gateway (Express)
├── micro_Ventas/       # Microservicio Ventas (FastAPI)
├── micro_Productos/    # Microservicio Productos (Express)
├── micro_Metricas/     # Microservicio Métricas (FastAPI)
└── frontend/           # Frontend (HTML + CSS + JS)
```

---

## 🚀 Instalación Rápida

### 1. Crear bases de datos

**MySQL:**
Abre una terminal y conecta a MySQL:
```bash
mysql -u root -p
password: root
```
Crea la base de datos (las tablas se crearán automáticamente):
```sql
CREATE DATABASE IF NOT EXISTS tpv_relacional;
SHOW DATABASES;
EXIT;
```

**MongoDB:**
Verifica que el servicio MongoDB esté corriendo (en PowerShell):
```powershell
Get-Service MongoDB
```
Si el Status es "Running", está listo. Si no está corriendo, inícialo:
```powershell
net start MongoDB
```
La base de datos y colecciones se crearán automáticamente al ejecutar los microservicios.

### 2. Instalar dependencias

**API Gateway y Productos (Node.js):**
```powershell
cd src/apiGateway; npm install
cd src/micro_Productos; npm install
```

**Ventas y Métricas (FastAPI):**
```powershell
cd src/micro_Ventas; pip install -r requirements.txt
cd src/micro_Metricas; pip install -r requirements.txt
```

### 3. Arrancar servicios

**Necesitas abrir 4 terminales separadas (una para cada microservicio):**

```powershell
# Terminal 1: API Gateway
cd src/apiGateway; npm start

# Terminal 2: Microservicio Productos
cd src/micro_Productos; npm start

# Terminal 3: Microservicio Ventas
cd src/micro_Ventas; python -m uvicorn main:app --reload --port 5001

# Terminal 4: Microservicio Métricas
cd src/micro_Metricas; python -m uvicorn main:app --reload --port 5003
```


---

## 🌐 Acceder a la Aplicación

**Frontend:** http://localhost:8080

**Documentación APIs:**
- Ventas: http://localhost:5001/docs
- Métricas: http://localhost:5003/docs

---

## 📝 Cambios respecto a la versión original

✅ **Eliminado**: Flask de todos los microservicios
✅ **Añadido**: FastAPI para Ventas y Métricas
✅ **Mantenido**: Express para API Gateway y Productos
✅ **Mejorado**: Documentación OpenAPI automática

---

Proyecto de la asignatura de Desarrollo web - Año 2025-2026