// Script de inicialización de productos por defecto
const mongoose = require('mongoose');
const Producto = require('./models/producto');

const productosIniciales = [
    { nombre: "Coca Cola", precio: 2.50, stock: 100, disponible: true },
    { nombre: "Agua Mineral", precio: 1.50, stock: 150, disponible: true },
    { nombre: "Cerveza Estrella", precio: 3.00, stock: 80, disponible: true },
    { nombre: "Café Solo", precio: 1.80, stock: 200, disponible: true },
    { nombre: "Café con Leche", precio: 2.20, stock: 200, disponible: true },
    { nombre: "Bocadillo Jamón", precio: 4.50, stock: 30, disponible: true },
    { nombre: "Bocadillo Queso", precio: 4.00, stock: 25, disponible: true },
    { nombre: "Ensalada Mixta", precio: 6.50, stock: 20, disponible: true },
    { nombre: "Pizza Margarita", precio: 8.90, stock: 15, disponible: true },
    { nombre: "Hamburguesa", precio: 7.50, stock: 25, disponible: true },
    { nombre: "Patatas Fritas", precio: 3.50, stock: 50, disponible: true },
    { nombre: "Tarta de Queso", precio: 5.00, stock: 12, disponible: true },
    { nombre: "Helado Vainilla", precio: 3.80, stock: 40, disponible: true },
    { nombre: "Zumo Naranja", precio: 2.80, stock: 60, disponible: true },
    { nombre: "Té Helado", precio: 2.50, stock: 70, disponible: true }
];

async function inicializarProductos() {
    try {
        // Contar productos existentes
        const count = await Producto.countDocuments();
        
        if (count === 0) {
            console.log('📦 Creando productos por defecto...');
            await Producto.insertMany(productosIniciales);
            console.log(`✅ ${productosIniciales.length} productos creados correctamente`);
        } else {
            console.log(`ℹ️  Ya existen ${count} productos en la base de datos`);
        }
    } catch (error) {
        console.error('❌ Error al inicializar productos:', error.message);
    }
}

module.exports = inicializarProductos;
