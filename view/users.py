from fastapi import APIRouter, HTTPException, Depends
from model.models import User, UserCreate, UserUpdate, AuthRequest, AuthResponse
from controller.database import users_collection
from bson import ObjectId
import logging
from controller.auth_utils import (
    create_access_token,
    get_current_user,
    invalidated_tokens,
    oauth2_scheme
)

router = APIRouter()

@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        logging.warning(f"Tentativa de criar usuário já existente: {user.username}")
        raise HTTPException(status_code=400, detail="Username já existe")
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "is_active": True
    }
    result = users_collection.insert_one(user_doc)
    logging.info(f"Usuário criado: {user.username} (id: {result.inserted_id})")
    return User(
        id=str(result.inserted_id),
        username=user.username,
        email=user.email,
        is_active=True
    )

@router.get("/users/{id}", response_model=User)
async def get_user(id: str, current_user: User = Depends(get_current_user)):
    try:
        user = users_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        logging.error(f"ID de usuário inválido: {id}")
        raise HTTPException(status_code=400, detail="Invalid user id")
    if user:
        logging.info(f"Usuário consultado: {id}")
        return User(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"],
            is_active=user["is_active"]
        )
    logging.warning(f"Usuário não encontrado: {id}")
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{id}", response_model=User)
async def update_user(id: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    update_data.pop("id", None)
    try:
        result = users_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    except Exception:
        logging.error(f"ID de usuário inválido para atualização: {id}")
        raise HTTPException(status_code=400, detail="Invalid user id")
    if result.matched_count == 0:
        logging.warning(f"Tentativa de atualizar usuário inexistente: {id}")
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = users_collection.find_one({"_id": ObjectId(id)})
    logging.info(f"Usuário atualizado: {id}")
    return User(
        id=str(updated_user["_id"]),
        username=updated_user["username"],
        email=updated_user["email"],
        is_active=updated_user["is_active"]
    )

@router.delete("/users/{id}")
async def delete_user(id: str, current_user: User = Depends(get_current_user)):
    try:
        result = users_collection.update_one({"_id": ObjectId(id)}, {"$set": {"is_active": False}})
    except Exception:
        logging.error(f"ID de usuário inválido para deleção: {id}")
        raise HTTPException(status_code=400, detail="Invalid user id")
    if result.matched_count == 0:
        logging.warning(f"Tentativa de deletar usuário inexistente: {id}")
        raise HTTPException(status_code=404, detail="User not found")
    logging.info(f"Usuário soft deleted: {id}")
    return {"message": f"User '{id}' soft deleted"}

# Auth endpoints
@router.post("/auth/login", response_model=AuthResponse)
async def login(auth: AuthRequest):
    user = users_collection.find_one({"username": auth.username, "is_active": True})
    if user and user["password"] == auth.password:
        access_token = create_access_token(data={"sub": str(user["_id"])})
        logging.info(f"Login realizado com sucesso para usuário: {auth.username}")
        return AuthResponse(access_token=access_token)
    elif user:
        logging.warning(f"Tentativa de login com senha incorreta para usuário: {auth.username}")
        raise HTTPException(status_code=401, detail="Senha incorreta")
    else:
        logging.warning(f"Tentativa de login para usuário inexistente: {auth.username}")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

@router.post("/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    invalidated_tokens.add(token)
    logging.info("Logout realizado com sucesso.")
    return {"message": "Logout realizado com sucesso."}