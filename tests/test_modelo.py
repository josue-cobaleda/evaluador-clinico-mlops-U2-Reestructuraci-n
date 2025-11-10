import sys
import os
from bs4 import BeautifulSoup  # Para leer HTML del render_template
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

# === TEST 1: Validar predicción leve ===
def test_prediccion_leve():
    cliente = app.test_client()
    datos = {
        "pcr": 5,
        "fc": 100,
        "edad": 25
    }
    # Enviar como formulario (no JSON)
    respuesta = cliente.post("/predecir", data=datos)
    
    # Validar código de respuesta
    assert respuesta.status_code == 200

    # Extraer el texto HTML y buscar el resultado en la página
    html = respuesta.data.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    assert "ENFERMEDAD LEVE" in soup.text


# === TEST 2: Validar que las predicciones se guarden y el historial funcione ===
def test_reporte_se_actualiza():
    cliente = app.test_client()

    # Limpiar logs antes de iniciar
    log_file = "logs/predicciones.csv"
    if os.path.exists(log_file):
        os.remove(log_file)

    # Hacer predicción
    datos = {"pcr": 30, "fc": 160, "edad": 90}
    cliente.post("/predecir", data=datos)

    # Consultar historial (HTML)
    resp = cliente.get("/historial")
    assert resp.status_code == 200

    # Verificar que contenga los datos esperados
    html = resp.data.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # Buscar palabras clave esperadas
    assert "ENFERMEDAD TERMINAL" in soup.text
    assert "Total por Categoría" in soup.text
    assert "Últimas 5 Predicciones" in soup.text
