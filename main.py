import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from pymongo import MongoClient
from bson import ObjectId
from config_URI import MONGO_URI

# Configuração do logging
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

client = MongoClient(MONGO_URI)
db = client["Grau_B"]

users_collection = db["users"]
tasks_collection = db["tasks"]

invalidated_tokens = set()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class User(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    status: str
    assigned_to: Optional[str] = None

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    assigned_to: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

app = FastAPI()

SECRET_KEY = "paodebatata"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

# --- User Endpoints ---

@app.post("/users", response_model=User)
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

@app.get("/users/{id}", response_model=User)
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

@app.put("/users/{id}", response_model=User)
async def update_user(id: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    update_data = {k: v for k, v in user.dict().items() if v is not None}
    update_data.pop("id", None)  # Garante que o id não será alterado
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

@app.delete("/users/{id}")
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

# --- Task Endpoints ---

@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user)):
    if not users_collection.find_one({"username": task.assigned_to, "is_active": True}):
        logging.warning(f"Tentativa de atribuir tarefa para usuário inexistente: {task.assigned_to}")
        raise HTTPException(status_code=400, detail="Assigned user does not exist")
    task_doc = {
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "assigned_to": task.assigned_to
    }
    result = tasks_collection.insert_one(task_doc)
    logging.info(f"Tarefa criada: {task.title} (id: {result.inserted_id}) atribuída para {task.assigned_to}")
    return Task(
        id=str(result.inserted_id),
        title=task.title,
        description=task.description,
        status=task.status,
        assigned_to=task.assigned_to
    )

@app.get("/tasks/{id}", response_model=Task)
async def get_task(id: str, current_user: User = Depends(get_current_user)):
    try:
        task = tasks_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        logging.error(f"ID de tarefa inválido: {id}")
        raise HTTPException(status_code=400, detail="Invalid task id")
    if not task:
        logging.warning(f"Tarefa não encontrada: {id}")
        raise HTTPException(status_code=404, detail="Task not found")
    logging.info(f"Tarefa consultada: {id}")
    return Task(
        id=str(task["_id"]),
        title=task["title"],
        description=task.get("description"),
        status=task["status"],
        assigned_to=task.get("assigned_to")
    )

@app.get("/tasks", response_model=List[Task])
async def list_tasks(assigned_to: Optional[str] = None, current_user: User = Depends(get_current_user)):
    query = {}
    if assigned_to:
        query["assigned_to"] = assigned_to
    tasks = []
    for task in tasks_collection.find(query):
        tasks.append(Task(
            id=str(task["_id"]),
            title=task["title"],
            description=task.get("description"),
            status=task["status"],
            assigned_to=task.get("assigned_to")
        ))
    logging.info(f"Listagem de tarefas. Filtro assigned_to: {assigned_to}")
    return tasks

@app.put("/tasks/{id}", response_model=Task)
async def update_task(id: str, task: TaskUpdate, current_user: User = Depends(get_current_user)):
    update_data = {k: v for k, v in task.dict().items() if v is not None}
    if "assigned_to" in update_data:
        if not users_collection.find_one({"username": update_data["assigned_to"], "is_active": True}):
            logging.warning(f"Tentativa de reatribuir tarefa para usuário inexistente: {update_data['assigned_to']}")
            raise HTTPException(status_code=400, detail="Assigned user does not exist")
    try:
        result = tasks_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    except Exception:
        logging.error(f"ID de tarefa inválido para atualização: {id}")
        raise HTTPException(status_code=400, detail="Invalid task id")
    if result.matched_count == 0:
        logging.warning(f"Tentativa de atualizar tarefa inexistente: {id}")
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = tasks_collection.find_one({"_id": ObjectId(id)})
    logging.info(f"Tarefa atualizada: {id}")
    return Task(
        id=str(updated_task["_id"]),
        title=updated_task["title"],
        description=updated_task.get("description"),
        status=updated_task["status"],
        assigned_to=updated_task.get("assigned_to")
    )

@app.delete("/tasks/{id}")
async def delete_task(id: str, current_user: User = Depends(get_current_user)):
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(id)})
    except Exception:
        logging.error(f"ID de tarefa inválido para deleção: {id}")
        raise HTTPException(status_code=400, detail="Invalid task id")
    if result.deleted_count == 0:
        logging.warning(f"Tentativa de deletar tarefa inexistente: {id}")
        raise HTTPException(status_code=404, detail="Task not found")
    logging.info(f"Tarefa deletada: {id}")
    return {"message": f"Task {id} deleted"}

# --- Auth Endpoints ---

@app.post("/auth/login", response_model=AuthResponse)
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

@app.post("/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    invalidated_tokens.add(token)
    logging.info("Logout realizado com sucesso.")
    return {"message": "Logout realizado com sucesso."}