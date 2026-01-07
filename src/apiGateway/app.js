const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const path = require('path');

const app = express();
const port = 8080;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../frontend')));

// Logging middleware
app.use((req, res, next) => {
    console.log(`📍 ${req.method} ${req.path}`);
    next();
});

// Información de estado del Gateway
app.get('/api/status', (req, res) => {
    res.json({
        status: 'ok',
        gateway: 'API Gateway (Express)',
        services: {
            ventas: 'http://localhost:5001',
            productos: 'http://localhost:5002',
            metricas: 'http://localhost:5003'
        }
    });
});

// Proxy a Microservicio de Ventas (FastAPI en puerto 5001)
app.use('/api/ventas', createProxyMiddleware({
    target: 'http://localhost:5001',
    changeOrigin: true,
    pathRewrite: {
        '^/api/ventas': '/ventas'
    },
    onProxyReq: (proxyReq, req, res) => {
        // Re-enviar el body parseado por express.json()
        if (req.body && Object.keys(req.body).length > 0) {
            const bodyData = JSON.stringify(req.body);
            proxyReq.setHeader('Content-Type', 'application/json');
            proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
            proxyReq.write(bodyData);
            proxyReq.end();
        }
    },
    onProxyRes: (proxyRes, req, res) => {
        console.log(`✅ Respuesta de Ventas: ${proxyRes.statusCode}`);
    },
    onError: (err, req, res) => {
        console.error('❌ Error en proxy Ventas:', err.message);
        res.status(500).json({ error: 'Error proxying to Ventas service' });
    }
}));

// Proxy a Microservicio de Productos (Express en puerto 5002)
app.use('/api/productos', createProxyMiddleware({
    target: 'http://localhost:5002',
    changeOrigin: true,
    pathRewrite: {
        '^/api/productos': '/productos'
    },
    onProxyReq: (proxyReq, req, res) => {
        // Re-enviar el body parseado por express.json()
        if (req.body && Object.keys(req.body).length > 0) {
            const bodyData = JSON.stringify(req.body);
            proxyReq.setHeader('Content-Type', 'application/json');
            proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
            proxyReq.write(bodyData);
            proxyReq.end();
        }
    },
    onProxyRes: (proxyRes, req, res) => {
        console.log(`✅ Respuesta de Productos: ${proxyRes.statusCode}`);
    },
    onError: (err, req, res) => {
        console.error('❌ Error en proxy Productos:', err.message);
        res.status(500).json({ error: 'Error proxying to Productos service' });
    }
}));

// Proxy a Microservicio de Métricas (FastAPI en puerto 5003)
app.use('/api/metricas', createProxyMiddleware({
    target: 'http://localhost:5003',
    changeOrigin: true,
    pathRewrite: {
        '^/api/metricas': '/metricas'
    },
    onProxyReq: (proxyReq, req, res) => {
        // Re-enviar el body parseado por express.json()
        if (req.body && Object.keys(req.body).length > 0) {
            const bodyData = JSON.stringify(req.body);
            proxyReq.setHeader('Content-Type', 'application/json');
            proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
            proxyReq.write(bodyData);
            proxyReq.end();
        }
    },
    onProxyRes: (proxyRes, req, res) => {
        console.log(`✅ Respuesta de Métricas: ${proxyRes.statusCode}`);
    },
    onError: (err, req, res) => {
        console.error('❌ Error en proxy Métricas:', err.message);
        res.status(500).json({ error: 'Error proxying to Metricas service' });
    }
}));

// Ruta raíz que sirve el frontend
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Manejo de errores global
app.use((err, req, res, next) => {
    console.error('❌ Error global:', err);
    res.status(500).json({ message: err.message });
});

app.listen(port, () => {
    console.log(`\n✅ API Gateway ejecutándose en http://localhost:${port}`);
    console.log(`\n📍 Rutas disponibles:`);
    console.log(`   GET  http://localhost:${port}/api/status`);
    console.log(`   POST http://localhost:${port}/api/ventas`);
    console.log(`   GET  http://localhost:${port}/api/productos`);
    console.log(`   POST http://localhost:${port}/api/productos`);
    console.log(`   GET  http://localhost:${port}/api/metricas\n`);
});
