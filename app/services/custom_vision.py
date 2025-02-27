import requests
import os
from dotenv import load_dotenv

load_dotenv()

PREDICTION_URL = os.getenv("AZURE_CUSTOM_VISION_ENDPOINT")
PREDICTION_KEY = os.getenv("AZURE_CUSTOM_VISION_KEY")

def analizar_imagen(image_path):
    """
    Envía una imagen a Azure Custom Vision y devuelve la predicción más alta.
    """
    headers = {
        "Content-Type": "application/octet-stream",
        "Prediction-Key": PREDICTION_KEY
    }
    
    with open(image_path, "rb") as image_data:
        response = requests.post(PREDICTION_URL, headers=headers, data=image_data)
    
    if response.status_code != 200:
        return {"error": "No se pudo procesar la imagen", "status": response.status_code}

    predictions = response.json().get("predictions", [])
    
    if not predictions:
        return {"error": "No se encontraron predicciones"}

    # 🔥 Obtener la predicción con mayor probabilidad
    best_prediction = max(predictions, key=lambda x: x["probability"])

    return {
        "tagName": best_prediction["tagName"],
        "probability": best_prediction["probability"]
    }
