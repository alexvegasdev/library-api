from flask import Flask
from app.database import db
from app.routes import api_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    db.init_app(app)

    # Registrar api_bp que ya incluye todas las rutas
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
