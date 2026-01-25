from flask import Flask, request, jsonify, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

#DB config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Modelo registro
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    mood = db.Column(db.String(50), nullable=False)
    nota = db.Column(db.String(200))

with app.app_context():
    db.create_all() 

#Rutas config
@app.route("/")
def home():
    return render_template("inicio.html")

@app.route("/registros")
def formulario():
    return render_template("registros.html")

@app.route("/registros", methods=["POST"])
def agregar_registro():
    datos = request.json
    
    nuevo = Registro(
        mood=datos.get("mood"),
        nota=datos.get("nota")
    )
    
    db.session.add(nuevo)
    db.session.commit()
    
    
    
    return jsonify({
        "message": "Registro agregado 🌱",
        "registro": {
            "id": nuevo.id,
            "fecha": nuevo.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "mood": nuevo.mood,
            "nota": nuevo.nota  
        }    
    })
    
@app.route("/registros/data", methods=["GET"])
def obtener_registros():
    todos = Registro.query.all()
    lista = []
    for r in todos:
        lista.append({
            "id": r.id,
            "fecha": r.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "mood": r.mood,
            "nota": r.nota
        })
    return jsonify(lista)

@app.route("/registros/<int:id>", methods=["GET"])
def get_registro_by_id(id):
    r = Registro.query.get(id)  
    if r is None:
        return jsonify({"error": "Registro no encontrado"}), 404

    return jsonify({
        "id": r.id,
        "fecha": r.fecha.strftime("%Y-%m-%d %H:%M:%S"),
        "mood": r.mood,
        "nota": r.nota
    })

@app.route("/registros/<int:id>", methods=["DELETE"])
def eliminar_registro(id):
    r = Registro.query.get(id)
    if r is None:
        return jsonify({"error": "Registro no encontrado"}), 404
    db.session.delete(r)
    db.session.commit()
    
    return jsonify({
    "message": "Registro eliminado 🌱",
    "id": id
})

    
if __name__ == "__main__":
    app.run(debug=True)
