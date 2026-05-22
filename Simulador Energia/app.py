from flask import Flask, render_template, request, jsonify, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)

ARCHIVO_CSV = "clientes_bioenergy.csv"

# =====================================================
# CREAR CSV SI NO EXISTE
# =====================================================

if not os.path.exists(ARCHIVO_CSV):
    with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([
            "Fecha",
            "Empresa",
            "Contacto",
            "Telefono",
            "Direccion",
            "Cantidad Equipos",
            "Cantidad KW",
            "Consumo Mensual KWh",
            "Ahorro Economico Mensual",
            "Ahorro Economico Anual",
            "Ahorro Economico 5 Anos",
            "Ahorro Economico 10 Anos",
            "Ahorro Economico 15 Anos"
        ])

# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")

# =====================================================
# GUARDAR CLIENTE
# =====================================================

@app.route("/guardar", methods=["POST"])
def guardar():
    data = request.json

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARCHIVO_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)

        writer.writerow([
            fecha,
            data.get("empresa"),
            data.get("contacto"),
            data.get("telefono"),
            data.get("direccion"),
            data.get("cantidad_equipos"),
            data.get("cantidad_kw"),
            data.get("consumo_kwh"),
            data.get("ahorro_mensual"),
            data.get("ahorro_anual"),
            data.get("ahorro_5"),
            data.get("ahorro_10"),
            data.get("ahorro_15")
        ])

    return jsonify({
        "mensaje": "Cliente guardado correctamente"
    })

# =====================================================
# DESCARGAR CSV
# =====================================================

@app.route("/descargar")
def descargar():
    return send_file(ARCHIVO_CSV, as_attachment=True)

# =====================================================
# MAIN (solo local)
# =====================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
