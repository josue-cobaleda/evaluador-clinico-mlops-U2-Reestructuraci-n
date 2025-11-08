# Evaluador Clinico - MLOps Unidad 2

## Problema
Desarrollar un servicio que permita a un médico realizar predicciones sobre el estado de un paciente (NO ENFERMO, LEVE, AGUDA, CRÓNICA), desplegado en Docker.

## Propósito
Simular un flujo de trabajo de MLOps para exponer un modelo médico simple como servicio web.

## Estructura inicial

servicio_medico/
├── app/
│ ├── app.py
│ ├── model.py
│ ├── train_model.py
├── model/
│ └── modelo_real.pkl
├── templates/
│ └── index.html
├── Dockerfile
├── requirements.txt
└── README.md


## Descripción
La solución permite al médico ingresar datos del paciente y recibir un diagnóstico simulado.  
Se despliega usando Docker y Flask.