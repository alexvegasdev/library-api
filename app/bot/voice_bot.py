import datetime
from app.models.book import Book
from app.models.author import Author

def saludar():
    """Saluda según la hora del día y presenta el bot."""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        saludo = "Buenos días!"
    elif hour < 18:
        saludo = "Buenas tardes!"
    else:
        saludo = "Buenas noches!"
    mensaje = f"{saludo} Soy LibraryBot, ¿en qué puedo ayudarte hoy?"
    return mensaje

def procesar_consulta(query):
    """
    Procesa la consulta y busca libros o autores en la base de datos.
    """
    query_lower = query.lower()
    respuesta = ""
    
    # Búsqueda de libros
    if "libro" in query_lower:
        if "muestrame libros" in query_lower or query_lower.strip() == "libro":
            books = Book.query.all()
            if books:
                respuesta = "Estos son los libros disponibles: " + ", ".join([f"{i+1}. {book.title}" for i, book in enumerate(books)])
            else:
                respuesta = "No hay libros disponibles."
        else:
            busqueda = query_lower.replace("muestrame", "").replace("buscar", "").replace("libro", "").strip()
            if busqueda:
                books = Book.query.filter(Book.title.ilike(f"%{busqueda}%")).all()
                if books:
                    respuesta = "Encontré los siguientes libros: " + ", ".join([f"{i+1}. {book.title}" for i, book in enumerate(books)])
                else:
                    respuesta = f"No encontré ningún libro que coincida con {busqueda}."
            else:
                respuesta = "No se especificó el nombre del libro."
    
    # Búsqueda de autores
    elif "autor" in query_lower:
        if "muestrame autores" in query_lower or query_lower.strip() == "autor":
            authors = Author.query.all()
            if authors:
                respuesta = "Estos son los autores disponibles: " + ", ".join([f"{i+1}. {author.name}" for i, author in enumerate(authors)])
            else:
                respuesta = "No hay autores disponibles."
        else:
            busqueda = query_lower.replace("muestrame", "").replace("buscar", "").replace("autor", "").strip()
            if busqueda:
                authors = Author.query.filter(Author.name.ilike(f"%{busqueda}%")).all()
                if authors:
                    respuesta = "Encontré los siguientes autores: " + ", ".join([f"{i+1}. {author.name}" for i, author in enumerate(authors)])
                else:
                    respuesta = f"No encontré ningún autor que coincida con {busqueda}."
            else:
                respuesta = "No se especificó el nombre del autor."
    else:
        respuesta = "Lo siento, no entendí tu consulta. Por favor, intenta decir 'muestrame libros' o 'muestrame autores'."
    
    return respuesta
