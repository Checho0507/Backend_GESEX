from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from ..utils.auth_utils import verify_google_token, create_jwt_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/auth/google")
async def login_with_google(token: str):
    """Ruta que recibe el token de Google desde el frontend"""
    try:
        # 1. Verificar token con Google
        user_data = verify_google_token(token)

        # 2. Crear JWT propio (sesión en tu sistema)
        access_token = create_jwt_token(user_data["email"])

        return {
            "access_token": access_token,
            "user": user_data
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, "Error interno")