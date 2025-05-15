import os
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración (usa variables de entorno en producción!)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")  # Obtener desde el .env
SECRET_KEY = os.getenv("SECRET_KEY")  # Obtener desde el .env
ALGORITHM = "HS256"

def verify_google_token(token: str):
    """Verifica el token de Google y devuelve datos del usuario"""
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        # Validación adicional (opcional)
        if not idinfo.get("email_verified", False):
            raise HTTPException(400, "Email no verificado por Google")

        return {
            "email": idinfo["email"],
            "name": idinfo.get("name", "Usuario"),
            "picture": idinfo.get("picture")
        }

    except ValueError as e:
        raise HTTPException(401, f"Token inválido: {str(e)}")

def create_jwt_token(email: str):
    """Crea un JWT para sesiones en tu sistema"""
    expires = datetime.utcnow() + timedelta(hours=2)
    payload = {
        "sub": email,
        "exp": expires
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
