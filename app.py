from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os


log_file = "logs/predicciones.txt"
os.makedirs("logs", exist_ok=True)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predecir', methods=['POST'])
def predecir():

    if request.is_json:
        datos = request.get_json()
        edad = int(datos.get('edad', 0))
        pcr = float(datos.get('pcr', 0))
        fc = int(datos.get('fc', 0))
    else:
        edad = int(request.form.get('edad', 0))
        pcr = float(request.form.get('pcr', 0))
        fc = int(request.form.get('fc', 0))

    # Simulación de un "modelo" con 5 categorías
    if pcr < 3 and fc < 90 and edad < 50:
        resultado = "NO ENFERMO"
    elif 3 <= pcr < 10 or 90 <= fc < 110:
        resultado = "ENFERMEDAD LEVE"
    elif 10 <= pcr < 20 or 110 <= fc < 130:
        resultado = "ENFERMEDAD AGUDA"
    elif 20 <= pcr < 25 or 130 <= fc < 150:
        resultado = "ENFERMEDAD CRÓNICA"
    else:
        resultado = "ENFERMEDAD TERMINAL"

    # Guardar la predicción con fecha y categoría
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()}, {resultado}\n")


    if request.is_json:
        return jsonify({
            "resultado": resultado,
            "edad": edad,
            "pcr": pcr,
            "fc": fc
        }), 200


    return render_template('index.html', resultado=resultado, edad=edad, pcr=pcr, fc=fc)

@app.route('/reporte', methods=['GET'])
def reporte():
    if not os.path.exists(log_file):
        return jsonify({"mensaje": "No hay predicciones registradas."})

    with open(log_file) as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]

    if not lineas:
        return jsonify({"mensaje": "No hay predicciones registradas."})

    total = len(lineas)
    categorias = {}
    for l in lineas:
        _, cat = l.split(", ")
        categorias[cat] = categorias.get(cat, 0) + 1

    ultimas = lineas[-5:]
    fecha_ultima = lineas[-1].split(",")[0]

    return jsonify({
        "total_predicciones": total,
        "por_categoria": categorias,
        "ultimas_5": ultimas,
        "ultima_fecha": fecha_ultima
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)