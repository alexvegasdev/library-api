import pyttsx3
import datetime
from app.models.book import Book
from app.models.author import Author

# Inicializa el motor de voz
engine = pyttsx3.init()
# Configura el idioma (opcional)
engine.setProperty("rate", 150)

def decir(texto):
    """Reproduce el texto en voz usando pyttsx3."""
    engine.say(texto)
    engine.runAndWait()

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
    decir(mensaje)
    return mensaje

def procesar_consulta(query):
    """
    Procesa la consulta de voz y busca libros o autores en la base de datos.
    Se esperan consultas como:
      - "muestrame libros"
      - "muestrame [algo] libro"
      - "muestrame autores"
      - "muestrame [algo] autor"
    """
    query_lower = query.lower()
    respuesta = ""
    
    # Busqueda de libros
    if "libro" in query_lower:
        # Si se menciona "muestrame libros" sin especificar
        if "muestrame libros" in query_lower or query_lower.strip() == "libro":
            books = Book.query.all()
            if books:
                respuesta = "Estos son los libros disponibles: " + ", ".join([book.title for book in books])
            else:
                respuesta = "No hay libros disponibles."
        else:
            # Si se menciona "muestrame [algo] libro"
            busqueda = query_lower.replace("muestrame", "").replace("buscar", "").replace("libro", "").strip()
            if busqueda:
                books = Book.query.filter(Book.title.ilike(f"%{busqueda}%")).all()
                if books:
                    respuesta = "Encontré los siguientes libros: " + ", ".join([book.title for book in books])
                else:
                    respuesta = f"No encontré ningún libro que coincida con {busqueda}."
            else:
                respuesta = "No se especificó el nombre del libro."
    
    # Busqueda de autores
    elif "autor" in query_lower:
        if "muestrame autores" in query_lower or query_lower.strip() == "autor":
            authors = Author.query.all()
            if authors:
                respuesta = "Estos son los autores disponibles: " + ", ".join([author.name for author in authors])
            else:
                respuesta = "No hay autores disponibles."
        else:
            busqueda = query_lower.replace("muestrame", "").replace("buscar", "").replace("autor", "").strip()
            if busqueda:
                authors = Author.query.filter(Author.name.ilike(f"%{busqueda}%")).all()
                if authors:
                    respuesta = "Encontré los siguientes autores: " + ", ".join([author.name for author in authors])
                else:
                    respuesta = f"No encontré ningún autor que coincida con {busqueda}."
            else:
                respuesta = "No se especificó el nombre del autor."
    else:
        respuesta = "Lo siento, no entendí tu consulta. Por favor, intenta decir 'muestrame libros' o 'muestrame autores'."
    
    # Opcionalmente, el bot también puede decir la respuesta:
    decir(respuesta)
    return respuesta

