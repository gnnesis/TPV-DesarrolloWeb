const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const port = 5002;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

// Logging middleware
app.use((req, res, next) => {
    console.log(`📍 ${req.method} ${req.path}`);
    next();
});

// Conexión a MongoDB con opciones mejoradas
const mongoURL = process.env.MONGODB_URL || 'mongodb://localhost:27017/tpv_nosql';
console.log(`🔗 Intentando conectar a MongoDB: ${mongoURL}`);

mongoose.connect(mongoURL, {
    serverSelectionTimeoutMS: 5000
})
    .then(async () => {
        console.log('✅ Conectado a MongoDB');
        // Inicializar productos por defecto
        const inicializarProductos = require('./seed');
        await inicializarProductos();
    })
    .catch(err => {
        console.error('❌ Error conectando a MongoDB:', err.message);
        console.error('⚠️  Asegúrate que mongod está ejecutándose');
    });

// Importar rutas
const productosRoutes = require('./routes/productos');

// Usar rutas
app.use('/productos', productosRoutes);

// Ruta de inicio
app.get('/', (req, res) => {
    res.json({
        status: 'ok',
        service: 'Microservicio de Productos',
        mongodb: mongoose.connection.readyState === 1 ? 'conectado' : 'desconectado',
        endpoints: {
            'GET /productos': 'Obtener todos los productos',
            'GET /productos/:id': 'Obtener un producto específico',
            'POST /productos': 'Crear un nuevo producto',
            'PUT /productos/:id': 'Actualizar un producto',
            'DELETE /productos/:id': 'Eliminar un producto'
        }
    });
});

// Manejo de errores global
app.use((err, req, res, next) => {
    console.error('❌ Error:', err);
    res.status(500).json({ message: err.message });
});

// Iniciar servidor
app.listen(port, () => {
    console.log(`\n✅ Servidor de productos ejecutándose en http://localhost:${port}`);
    console.log(`📍 GET  http://localhost:${port}/productos\n`);
});