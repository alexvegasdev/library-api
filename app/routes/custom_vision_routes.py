import os
from flask import Blueprint, request, jsonify
from app.services.custom_vision import analizar_imagen
from app.models.book import Book

custom_vision_bp = Blueprint("custom_vision", __name__)

UPLOAD_FOLDER = "temp"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

THRESHOLD = 0.9  # 🔥 Umbral mínimo de confianza

@custom_vision_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "El archivo está vacío"}), 400

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    result = analizar_imagen(image_path)

    if "error" in result:
        os.remove(image_path)  # 🔥 Borra la imagen si hubo error
        return jsonify(result), 400

    probability = result["probability"]
    
    # 🔥 Verifica si la confianza es suficiente
    if probability < THRESHOLD:
        os.remove(image_path)
        return jsonify({
            "message": "La predicción no es lo suficientemente confiable",
            "predicted_title": result["tagName"],
            "probability": probability
        }), 200

    predicted_title = result["tagName"]
    book = Book.query.filter(Book.title.ilike(f"%{predicted_title}%")).first()

    response_data = {
        "message": "No se encontró un libro con este título",
        "predicted_title": predicted_title,
        "probability": probability
    }

    if book:
        response_data = {
            "predicted_book": book.title,
            "authors": [author.name for author in book.authors],
            "stock": book.stock,
            "cover_url": book.cover_url,
            "probability": probability
        }

    os.remove(image_path)  # 🔥 Borra la imagen después de procesarla
    return jsonify(response_data)
