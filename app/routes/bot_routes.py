from flask import Blueprint, jsonify, request
from app.bot.voice_bot import saludar, procesar_consulta

bot_bp = Blueprint('bot', __name__)

@bot_bp.route('/start', methods=['POST'])
def iniciar():
    """
    Ruta para iniciar el bot.
    Se espera un JSON con:
      - res: "SI"
      - sal: "CONSALUDO" (o cualquier otro valor para no saludar)
    """
    data = request.json
    res = data.get('res')
    sal = data.get('sal')
    if res == "SI":
        if sal == "CONSALUDO":
            mensaje = saludar()
        else:
            mensaje = "Bienvenido, soy LibraryBot. ¿En qué puedo ayudarte?"
        return jsonify({"status": "success", "message": mensaje})
    return jsonify({"status": "error", "message": "No se pudo iniciar el asistente"})

@bot_bp.route('/speech', methods=['POST'])
def consulta():
    """
    Ruta para procesar una consulta de voz (ya convertida a texto).
    Se espera un JSON con:
      - query: El texto de la consulta.
    """
    data = request.json
    query = data.get('query')
    if query:
        respuesta = procesar_consulta(query)
        return jsonify({"status": "success", "respuesta": respuesta})
    else:
        return jsonify({"status": "error", "message": "No se recibió consulta"})
