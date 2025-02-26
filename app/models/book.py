from app.database import db
from .author import book_author

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=1)
    authors = db.relationship('Author', secondary=book_author, back_populates='books')
