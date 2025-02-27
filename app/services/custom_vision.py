import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales de Custom Vision desde .env
PREDICTION_URL = os.getenv("AZURE_CUSTOM_VISION_ENDPOINT")
PREDICTION_KEY = os.getenv("AZURE_CUSTOM_VISION_KEY")

def analizar_imagen(image_path):
    """
    Envía una imagen a Azure Custom Vision y devuelve las predicciones.
    """
    headers = {
        "Content-Type": "application/octet-stream",
        "Prediction-Key": PREDICTION_KEY
    }
    
    with open(image_path, "rb") as image_data:
        response = requests.post(PREDICTION_URL, headers=headers, data=image_data)
    
    if response.status_code == 200:
        return response.json()  # Devuelve los resultados en JSON
    else:
        return {"error": "No se pudo procesar la imagen", "status": response.status_code}
