from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from ..config import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_current_user_id(credentials=Depends(security)) -> str:
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="No user_id in token")
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
