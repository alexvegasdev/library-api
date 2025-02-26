from flask import Blueprint, jsonify, request
from app.database import db
from app.models.author import Author

author_bp = Blueprint('authors', __name__)

# Obtener todos los autores
@author_bp.route('/', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify([{ "id": a.id, "name": a.name } for a in authors])

# Obtener un autor por ID
@author_bp.route('/<int:id>', methods=['GET'])
def get_author(id):
    author = Author.query.get_or_404(id)
    return jsonify({ "id": author.id, "name": author.name })

# Crear un nuevo autor
@author_bp.route('/', methods=['POST'])
def create_author():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    
    author = Author(name=data['name'])
    db.session.add(author)
    db.session.commit()
    return jsonify({"message": "Author created successfully", "id": author.id}), 201

# Actualizar un autor por ID (solo nombre)
@author_bp.route('/<int:id>', methods=['PUT'])
def update_author(id):
    author = Author.query.get_or_404(id)
    data = request.json
    if "name" in data:
        author.name = data["name"]
        db.session.commit()
        return jsonify({"message": "Author updated successfully"})
    return jsonify({"error": "Nothing to update"}), 400

# Eliminar un autor por ID
@author_bp.route('/<int:id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": "Author deleted successfully"})
