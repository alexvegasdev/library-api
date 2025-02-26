from flask import Blueprint, jsonify, request
from app.database import db
from app.models.book import Book
from app.models.author import Author

book_bp = Blueprint('books', __name__)

# Obtener todos los libros con sus autores
@book_bp.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        "id": book.id,
        "title": book.title,
        "cover_url": book.cover_url,
        "description": book.description,
        "stock": book.stock,  # Agregado stock
        "authors": [{"id": a.id, "name": a.name} for a in book.authors]
    } for book in books])

# Obtener un libro por ID con sus autores
@book_bp.route('/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        "id": book.id,
        "title": book.title,
        "cover_url": book.cover_url,
        "description": book.description,
        "stock": book.stock,  # Agregado stock
        "authors": [{"id": a.id, "name": a.name} for a in book.authors]
    })

# Crear un nuevo libro con autores asociados
@book_bp.route('/', methods=['POST'])
def create_book():
    data = request.json
    if not data or "title" not in data or "author_ids" not in data:
        return jsonify({"error": "Title and author_ids are required"}), 400
    
    book = Book(
        title=data['title'],
        cover_url=data.get('cover_url', ''),
        description=data.get('description', ''),
        stock=data.get('stock', 1)  # Agregado stock con valor por defecto
    )

    # Asociar autores al libro
    authors = Author.query.filter(Author.id.in_(data["author_ids"])).all()
    if not authors:
        return jsonify({"error": "Authors not found"}), 400
    
    book.authors.extend(authors)
    db.session.add(book)
    db.session.commit()
    
    return jsonify({"message": "Book created successfully", "id": book.id}), 201

# Actualizar un libro por ID (incluyendo autores)
@book_bp.route('/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.json

    if "title" in data:
        book.title = data["title"]
    if "cover_url" in data:
        book.cover_url = data["cover_url"]
    if "description" in data:
        book.description = data["description"]
    if "stock" in data:
        book.stock = data["stock"]  # Se puede actualizar stock

    if "author_ids" in data:
        authors = Author.query.filter(Author.id.in_(data["author_ids"])).all()
        book.authors = authors
    
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})

# Eliminar un libro por ID
@book_bp.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})

# Actualizar parcialmente un libro por ID (PATCH)
@book_bp.route('/<int:id>', methods=['PATCH'])
def patch_book(id):
    book = Book.query.get_or_404(id)
    data = request.json

    if "title" in data:
        book.title = data["title"]
    if "cover_url" in data:
        book.cover_url = data["cover_url"]
    if "description" in data:
        book.description = data["description"]
    if "stock" in data:
        book.stock = data["stock"]  # Se puede actualizar stock

    if "author_ids" in data:
        authors = Author.query.filter(Author.id.in_(data["author_ids"])).all()
        book.authors = authors
    
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})
