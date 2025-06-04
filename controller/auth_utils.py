import logging
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from controller.database import users_collection
from model.models import User

SECRET_KEY = "paodebatata"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

invalidated_tokens = set()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in invalidated_tokens:
        logging.warning("Token inválido ou expirado usado para autenticação.")
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            logging.warning("Tentativa de autenticação com credenciais inválidas.")
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        user = users_collection.find_one({"_id": ObjectId(user_id), "is_active": True})
        if user:
            return User(
                id=str(user["_id"]),
                username=user["username"],
                email=user["email"],
                is_active=user["is_active"]
            )
        logging.warning(f"Usuário não encontrado para o id: {user_id}")
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    except JWTError:
        logging.warning("Token JWT inválido ou expirado.")
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")