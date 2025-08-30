# account_service/app/accounts/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import Account

import os

security = HTTPBearer()


def get_current_user(credentials=Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

def decode_token(token: str) -> dict:
    """
    Decodifica el JWT usando HS256 (o el algoritmo indicado por settings).
    Espera encontrar 'user_id' o 'sub' en el payload.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_id(credentials=Depends(security)) -> int:
    """
    Extrae el user_id del JWT. Acepta 'user_id' o 'sub' como claim.
    """
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("user_id") or payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="No user_id in token")
    if isinstance(user_id, str) and user_id.isdigit():
        user_id = int(user_id)
    return user_id

def ensure_account_owner(
    account_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
) -> Account:
    """
    Verifica que la cuenta exista y pertenezca al usuario autenticado.
    Retorna la entidad Account cuando pasa la validación.
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None or account.user_id != current_user_id:
        # Para no filtrar existencia, devolvemos 404 si no es del usuario
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account
