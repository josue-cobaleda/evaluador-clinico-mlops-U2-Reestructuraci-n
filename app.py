from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predecir', methods=['POST'])


def predecir():
    edad = int(request.form['edad'])
    pcr = float(request.form['pcr'])
    fc = int(request.form['fc'])

    # Simulación de un "modelo"
    if pcr < 3 and fc < 90 and edad < 50:
        resultado = "NO ENFERMO"
    elif 3 <= pcr < 10 or 90 <= fc < 110:
        resultado = "ENFERMEDAD LEVE"
    elif 10 <= pcr < 20 or 110 <= fc < 130:
        resultado = "ENFERMEDAD AGUDA"
    else:
        resultado = "ENFERMEDAD CRÓNICA"

    return render_template('index.html', resultado=resultado, edad=edad, pcr=pcr, fc=fc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
