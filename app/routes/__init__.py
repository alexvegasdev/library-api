from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .book_routes import book_bp
from .author_routes import author_bp

api_bp.register_blueprint(book_bp, url_prefix='/books')
api_bp.register_blueprint(author_bp, url_prefix='/authors')
