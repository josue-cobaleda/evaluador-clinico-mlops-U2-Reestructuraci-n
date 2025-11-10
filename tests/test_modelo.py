import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
import os
import requests

# Validar que genere predicciones
def test_prediccion_leve():
    cliente = app.test_client()
    datos = {
        "pcr": 5,
        "fc": 100,
        "edad": 25
    }
    respuesta = cliente.post("/predecir", json=datos)
    assert respuesta.status_code == 200
    assert "ENFERMEDAD LEVE" in respuesta.json["resultado"]

# Validarlas predicciones se guarden
def test_reporte_se_actualiza():
    cliente = app.test_client()

    # Limpiar logs antes de iniciar
    if os.path.exists("logs/predicciones.txt"):
        os.remove("logs/predicciones.txt")

    # Hacer predicción
    datos = {"pcr": 30, "fc": 160, "edad": 90}
    cliente.post("/predecir", json=datos)

    # Consultar reporte
    resp = cliente.get("/reporte")
    data = resp.json

    assert data["total_predicciones"] >= 1
    assert "ENFERMEDAD TERMINAL" in str(data["por_categoria"])
