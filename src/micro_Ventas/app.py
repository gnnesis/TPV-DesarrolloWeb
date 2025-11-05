from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# Configuración de la BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/tpv_relacional'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesa = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=date.today)
    total = db.Column(db.Float, nullable=False)
    comandas = db.relationship('Comanda', backref='venta', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'mesa': self.mesa,
            'fecha': self.fecha.isoformat(),
            'total': self.total,
            'comandas': [comanda.to_dict() for comanda in self.comandas]
        }

class Comanda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    producto_id = db.Column(db.String(50), nullable=False)  # ID del producto en MongoDB
    cantidad = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad
        }

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# Endpoints para Ventas
@app.route('/ventas', methods=['GET'])
def get_ventas():
    ventas = Venta.query.all()
    return jsonify([venta.to_dict() for venta in ventas])

@app.route('/ventas/<int:id>', methods=['GET'])
def get_venta(id):
    venta = Venta.query.get_or_404(id)
    return jsonify(venta.to_dict())

@app.route('/ventas', methods=['POST'])
def create_venta():
    data = request.get_json()
    
    # Crear la venta
    nueva_venta = Venta(
        mesa=data['mesa'],
        total=data['total']
    )
    db.session.add(nueva_venta)
    
    # Crear las comandas asociadas
    for comanda_data in data.get('comandas', []):
        comanda = Comanda(
            producto_id=comanda_data['producto_id'],
            cantidad=comanda_data['cantidad']
        )
        nueva_venta.comandas.append(comanda)
    
    db.session.commit()
    return jsonify(nueva_venta.to_dict()), 201

# Endpoints para Comandas
@app.route('/ventas/<int:venta_id>/comandas', methods=['GET'])
def get_comandas(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    return jsonify([comanda.to_dict() for comanda in venta.comandas])

@app.route('/ventas/<int:venta_id>/comandas', methods=['POST'])
def add_comanda(venta_id):
    venta = Venta.query.get_or_404(venta_id)
    data = request.get_json()
    
    nueva_comanda = Comanda(
        venta_id=venta_id,
        producto_id=data['producto_id'],
        cantidad=data['cantidad']
    )
    
    db.session.add(nueva_comanda)
    db.session.commit()
    
    return jsonify(nueva_comanda.to_dict()), 201

# Ruta principal que muestra la interfaz web
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
