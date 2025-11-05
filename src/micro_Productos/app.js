const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');

const app = express();
const port = 5002; // Puerto diferente al de Ventas

// Middleware
app.use(cors()); // Permitir peticiones desde otros dominios
app.use(express.json()); // Para poder recibir JSON en las peticiones

// Conexión a MongoDB
mongoose.connect('mongodb://localhost:27017/tpv_productos')
    .then(() => console.log('Conectado a MongoDB'))
    .catch(err => console.error('Error conectando a MongoDB:', err));

// Importar rutas
const productosRoutes = require('./routes/productos');

// Usar rutas
app.use('/productos', productosRoutes);

// Configurar el motor de plantillas
app.set('views', path.join(__dirname, 'templates'));
app.set('view engine', 'html');
app.engine('html', require('ejs').renderFile);

// Ruta de inicio
app.get('/', (req, res) => {
    res.render('index');
});

// Iniciar servidor
app.listen(port, () => {
    console.log(`Servidor de productos ejecutándose en http://localhost:${port}`);
});