const mongoose = require('mongoose');

const productoSchema = new mongoose.Schema({
    nombre: {
        type: String,
        required: true,
        trim: true
    },
    precio: {
        type: Number,
        required: true,
        min: 0
    },
    disponible: {
        type: Boolean,
        default: true
    }
}, {
    timestamps: true // Añade automáticamente campos createdAt y updatedAt
});

module.exports = mongoose.model('Producto', productoSchema);