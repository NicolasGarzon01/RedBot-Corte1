# auth_service/app/auth/dependencies.py

from typing import Generator
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt

from ..config import JWT_SECRET, JWT_ALGORITHM
from ..database import SessionLocal
from .models import User
from jwt import ExpiredSignatureError, InvalidTokenError

security = HTTPBearer()  # extrae automáticamente Authorization: Bearer <token>

def get_db() -> Generator[Session, None, None]:
    """
    Dependencia para obtener una sesión de DB.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def decode_token(token: str) -> dict:
    """
    Decodifica y verifica el JWT. Lanza HTTPException si no es válido.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependencia que devuelve el objeto User asociado al token.
    Lanza 401 si el token es inválido o no existe el usuario.
    """
    token = credentials.credentials
    payload = decode_token(token)

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido: falta 'sub'")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return user

def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependencia que asegura que el usuario actual tenga rol 'admin'.
    Lanza 403 si no es admin.
    """
    if getattr(current_user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado: requiere rol admin")
    return current_user
