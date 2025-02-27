import os
from flask import Blueprint, request, jsonify
from app.services.custom_vision import analizar_imagen

custom_vision_bp = Blueprint("custom_vision", __name__)

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@custom_vision_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "El archivo está vacío"}), 400

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # 🔥 Llamar a Azure Custom Vision para analizar la imagen
    result = analizar_imagen(image_path)

    return jsonify(result)
