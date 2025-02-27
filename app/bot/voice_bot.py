import datetime
import unicodedata
from app.models.book import Book
from app.models.author import Author

def normalizar_texto(texto):
    """Convierte el texto a minúsculas y elimina tildes."""
    texto = texto.lower()
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")

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
    query_normalizada = normalizar_texto(query)
    respuesta = ""

    # Búsqueda de libros
    if "libro" in query_normalizada:
        if "muestrame libros" in query_normalizada or query_normalizada.strip() == "libro":
            books = Book.query.all()
            if books:
                respuesta = "Estos son los libros disponibles: " + ", ".join([f"{i+1}. {book.title}" for i, book in enumerate(books)])
            else:
                respuesta = "No hay libros disponibles."
        else:
            busqueda = query_normalizada.replace("muestrame", "").replace("buscar", "").replace("libro", "").strip()
            if busqueda:
                books = Book.query.filter(Book.title.ilike(f"%{busqueda}%")).all()
                if books:
                    detalles = []
                    for book in books:
                        autores = ", ".join([author.name for author in book.authors])
                        detalles.append(f"{book.title} - Autor(es): {autores} - Stock: {book.stock} disponibles")
                    respuesta = "Encontré los siguientes libros:\n" + "\n".join(detalles)
                else:
                    respuesta = f"No encontré ningún libro que coincida con '{busqueda}'."
            else:
                respuesta = "No se especificó el nombre del libro."

    # Búsqueda de autores
    elif "autor" in query_normalizada:
        if "muestrame autores" in query_normalizada or query_normalizada.strip() == "autor":
            authors = Author.query.all()
            if authors:
                respuesta = "Estos son los autores disponibles: " + ", ".join([f"{i+1}. {author.name}" for i, author in enumerate(authors)])
            else:
                respuesta = "No hay autores disponibles."
        else:
            busqueda = query_normalizada.replace("muestrame", "").replace("buscar", "").replace("autor", "").strip()
            if busqueda:
                authors = Author.query.filter(Author.name.ilike(f"%{busqueda}%")).all()
                if authors:
                    detalles = []
                    for author in authors:
                        libros = ", ".join([book.title for book in author.books])
                        detalles.append(f"{author.name} - Libros: {libros if libros else 'No tiene libros registrados'}")
                    respuesta = "Encontré los siguientes autores:\n" + "\n".join(detalles)
                else:
                    respuesta = f"No encontré ningún autor que coincida con '{busqueda}'."
            else:
                respuesta = "No se especificó el nombre del autor."
    else:
        respuesta = "Lo siento, no entendí tu consulta. Por favor, intenta decir 'muéstrame libros' o 'muéstrame autores'."
    
    return respuesta
