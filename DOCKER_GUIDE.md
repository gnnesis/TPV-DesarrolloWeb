# 🐳 Docker Compose - Guía de Uso

## 📋 Prerrequisitos

Antes de usar Docker Compose, asegúrate de tener instalado:

- **Docker Desktop** (incluye Docker y Docker Compose)
  - Windows: https://www.docker.com/products/docker-desktop
  - Verifica instalación: `docker --version` y `docker-compose --version`

## 🚀 Comandos para ejecutar el proyecto

### Iniciar todos los servicios

```bash
docker-compose up
```

Este comando:
- ✅ Construye las imágenes Docker de todos los microservicios
- ✅ Inicia MySQL y MongoDB
- ✅ Inicia los 4 microservicios automáticamente
- ✅ Muestra los logs de todos los servicios en tiempo real

### Iniciar en segundo plano (modo detached)

```bash
docker-compose up -d
```

### Ver logs de todos los servicios

```bash
docker-compose logs -f
```

### Ver logs de un servicio específico

```bash
docker-compose logs -f gateway
docker-compose logs -f ventas
docker-compose logs -f productos
docker-compose logs -f metricas
```

### Detener todos los servicios

```bash
docker-compose down
```

### Detener y eliminar todo (incluyendo volúmenes de bases de datos)

```bash
docker-compose down -v
```

### Reconstruir las imágenes (después de cambios en el código)

```bash
docker-compose up --build
```

### Ver estado de los contenedores

```bash
docker-compose ps
```

## 🌐 Acceder a los servicios

Una vez que ejecutes `docker-compose up`, los servicios estarán disponibles en:

| Servicio | URL | Puerto |
|----------|-----|--------|
| **Frontend** | http://localhost:8080 | 8080 |
| **API Gateway** | http://localhost:8080/api/status | 8080 |
| **Microservicio Ventas** | http://localhost:5001 | 5001 |
| **Microservicio Productos** | http://localhost:5002 | 5002 |
| **Microservicio Métricas** | http://localhost:5003 | 5003 |
| **MySQL** | localhost:3306 | 3306 |
| **MongoDB** | localhost:27017 | 27017 |

## 📁 Estructura de contenedores

```
┌─────────────────┐
│   API Gateway   │  :8080
│   (Node.js)     │
└────────┬────────┘
         │
    ┌────┴────────────────────────┐
    │                             │
┌───▼──────┐  ┌─────▼──────┐  ┌──▼────────┐
│  Ventas  │  │ Productos  │  │ Métricas  │
│ (FastAPI)│  │ (Node.js)  │  │ (FastAPI) │
│  :5001   │  │   :5002    │  │   :5003   │
└────┬─────┘  └─────┬──────┘  └─────┬─────┘
     │              │               │
┌────▼─────┐  ┌────▼──────┐         │
│  MySQL   │  │  MongoDB  │         │
│  :3306   │  │  :27017   │─────────┘
└──────────┘  └───────────┘
```

## 🔧 Solución de problemas

### Error: "port is already allocated"
Si algún puerto ya está en uso, detén el proceso que lo está usando o cambia el puerto en `docker-compose.yml`.

```bash
# Ver qué proceso usa un puerto (PowerShell)
netstat -ano | findstr :8080
```

### Recrear todo desde cero
Si hay problemas, elimina todo y vuelve a empezar:

```bash
docker-compose down -v
docker-compose up --build
```

### Ver detalles de un contenedor específico

```bash
docker logs tpv-gateway
docker logs tpv-ventas
docker logs tpv-productos
docker logs tpv-metricas
docker logs tpv-mysql
docker logs tpv-mongodb
```

### Entrar dentro de un contenedor

```bash
docker exec -it tpv-gateway sh
docker exec -it tpv-mysql mysql -u root -proot
docker exec -it tpv-mongodb mongosh
```

## Persistencia de datos

Los datos de las bases de datos se guardan en **volúmenes de Docker**:
- `mysql_data`: Datos de MySQL
- `mongodb_data`: Datos de MongoDB

Estos volúmenes persisten incluso después de detener los contenedores con `docker-compose down`.

Para eliminar los datos y empezar de cero, usa:
```bash
docker-compose down -v
```

## 🔄 Actualizar el código

Si haces cambios en el código:

1. Detén los contenedores: `docker-compose down`
2. Reconstruye y reinicia: `docker-compose up --build`

O para cambios rápidos, reinicia solo un servicio:
```bash
docker-compose restart gateway
docker-compose restart ventas
```

---


