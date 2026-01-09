# TPV GB - Sistema de Punto de Venta (Microservicios)

Sistema de Punto de Venta basado en **arquitectura de microservicios** para gestión de ventas, productos y analíticas en tiempo real.

---

##  Arquitectura de Microservicios

| Componente | Tecnología | Puerto | Base de Datos |
|---|---|---|---|
| **API Gateway** | Node.js + Express | 8080 | - |
| **Microservicio Ventas** | FastAPI (Python) | 5001 | MySQL |
| **Microservicio Productos** | Node.js + Express | 5002 | MongoDB |
| **Microservicio Métricas** | FastAPI (Python) | 5003 | MySQL |
| **Base de datos relacional** | MySQL 8.0 | 3306 | - |
| **Base de datos NoSQL** | MongoDB 7.0 | 27017 | - |

### Características principales:
-  **2 microservicios en Python** (Ventas y Métricas con FastAPI)
-  **2 microservicios en Node.js** (API Gateway y Productos con Express)
-  **API RESTful** con documentación OpenAPI 3.0 automática
-  **Base de datos híbrida**: MySQL (relacional) + MongoDB (NoSQL)
-  **API Gateway centralizado** que enruta a los microservicios
-  **SPA (Single Page Application)** con HTML5 + JavaScript vanilla
-  **Docker Compose** para orquestación de contenedores

---

## Estructura del Proyecto

```
TPV-DesarrolloWeb/
├── presentation/           # Presentación PowerPoint del proyecto
├── src/
│   ├── apiGateway/        # API Gateway (Express) - Puerto 8080
│   ├── micro_Ventas/      # Microservicio Ventas (FastAPI) - Puerto 5001
│   ├── micro_Productos/   # Microservicio Productos (Express) - Puerto 5002
│   ├── micro_Metricas/    # Microservicio Métricas (FastAPI) - Puerto 5003
│   └── frontend/          # Frontend SPA (HTML5 + CSS + JavaScript)
├── docker-compose.yml     # Orquestación de contenedores
├── DOCKER_GUIDE.md        # Guía detallada de Docker
└── README.md              # Este archivo
```

---

## Instalación y Ejecución

### Método 1: Docker Compose (RECOMENDADO)

**Software necesario:**
- Docker Desktop (incluye Docker y Docker Compose)
  - Descarga: https://www.docker.com/products/docker-desktop

#### Pasos para ejecutar:

1. **Abrir Docker Desktop** y esperar a que se inicie completamente

2. **Ejecutar el proyecto** (desde la raíz del proyecto):
```bash
docker-compose up
```

3. **Acceder a la aplicación:**
   - Frontend: http://localhost:8080
   - API Ventas: http://localhost:5001/docs
   - API Métricas: http://localhost:5003/docs

**Comandos útiles:**
```bash
# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener todo
docker-compose down

# Reiniciar (con reconstrucción)
docker-compose up --build
```

---

### Método 2: Ejecución Manual (Desarrollo)

**Software necesario:**
1. **Python 3.10+** - https://www.python.org/downloads/
2. **Node.js v16+** - https://nodejs.org/
3. **MySQL 8.0** - https://dev.mysql.com/downloads/mysql/
4. **MongoDB 7.0** - https://www.mongodb.com/try/download/community

**Verificar instalaciones:**
```bash
python --version
node --version
mysql --version
mongod --version
```

#### Paso 1: Crear bases de datos

**MySQL:**
```bash
mysql -u root -p
```
```sql
CREATE DATABASE IF NOT EXISTS tpv_relacional;
EXIT;
```

**MongoDB:**
Se crea automáticamente al arrancar el microservicio de productos.

#### Paso 2: Instalar dependencias

**Microservicios Node.js:**
```bash
cd src/apiGateway
npm install

cd ../micro_Productos
npm install
```

**Microservicios Python:**
```bash
cd src/micro_Ventas
pip install -r requirements.txt

cd ../micro_Metricas
pip install -r requirements.txt
```

#### Paso 3: Arrancar servicios

**Abrir 4 terminales separadas:**

```bash
# Terminal 1: API Gateway
cd src/apiGateway
npm start

# Terminal 2: Microservicio Productos
cd src/micro_Productos
npm start

# Terminal 3: Microservicio Ventas
cd src/micro_Ventas
uvicorn main:app --reload --port 5001

# Terminal 4: Microservicio Métricas
cd src/micro_Metricas
uvicorn main:app --reload --port 5003
```

#### Paso 4: Acceder a la aplicación
- **Frontend:** http://localhost:8080
- **API Ventas:** http://localhost:5001/docs
- **API Métricas:** http://localhost:5003/docs

---

##  Documentación Adicional

- [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Guía completa de Docker Compose

---

##  Proyecto de la Asignatura

**Desarrollo Web - Curso 2025-2026**