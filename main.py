from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

users_db = {}
user_passwords = {}
user_id_counter = 1

invalidated_tokens = set()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

tasks_db = {}
task_id_counter = 1

# User and Task models
class User(BaseModel):
    id: int
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
    id: int
    title: str
    description: Optional[str] = None
    status: str
    assigned_to: Optional[str] = None   # username

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

SECRET_KEY = "paodebatata"  # Troque por uma chave forte em produção!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token in invalidated_tokens:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        for user in users_db.values():
            if user.username == username and user.is_active:
                return user
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

# --- User Endpoints ---
@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    global user_id_counter
    user_obj = User(
        id=user_id_counter,
        username=user.username,
        email=user.email,
        is_active=True
    )
    users_db[user_id_counter] = user_obj
    user_passwords[user_id_counter] = user.password
    user_id_counter += 1
    return user_obj

@app.get("/users/{username}", response_model=User)
async def get_user(username: str, current_user: User = Depends(get_current_user)):
    for user in users_db.values():
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{username}", response_model=User)
async def update_user(username: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    # Find the user by username
    for user_id, stored_user in users_db.items():
        if stored_user.username == username:
            updated_data = user.dict(exclude_unset=True)
            updated_user = stored_user.copy(update=updated_data)
            users_db[user_id] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{username}")
async def delete_user(username: str, current_user: User = Depends(get_current_user)):
    for user_id, stored_user in users_db.items():
        if stored_user.username == username:
            # Soft delete: set is_active to False
            updated_user = stored_user.copy(update={"is_active": False})
            users_db[user_id] = updated_user
            return {"message": f"User '{username}' soft deleted"}
    raise HTTPException(status_code=404, detail="User not found")


# --- Task Endpoints ---
@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user)):
    global task_id_counter
    # Validate assigned_to if provided
    if task.assigned_to is not None:
        if not any(u.username == task.assigned_to for u in users_db.values()):
            raise HTTPException(status_code=400, detail="Assigned user does not exist")
    task_obj = Task(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        status=task.status,
        assigned_to=task.assigned_to
    )
    tasks_db[task_id_counter] = task_obj
    task_id_counter += 1
    return task_obj

@app.get("/tasks/{id}", response_model=Task)
async def get_task(id: int, current_user: User = Depends(get_current_user)):
    task = tasks_db.get(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/tasks", response_model=List[Task])
async def list_tasks(assigned_to: Optional[str] = None, current_user: User = Depends(get_current_user)):
    if assigned_to:
        return [task for task in tasks_db.values() if task.assigned_to == assigned_to]
    return list(tasks_db.values())

@app.put("/tasks/{id}", response_model=Task)
async def update_task(id: int, task: TaskUpdate, current_user: User = Depends(get_current_user)):
    stored_task = tasks_db.get(id)
    if not stored_task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_data = task.dict(exclude_unset=True)
    # Validate assigned_to if provided
    if "assigned_to" in updated_data and updated_data["assigned_to"] is not None:
        if not any(u.username == updated_data["assigned_to"] for u in users_db.values()):
            raise HTTPException(status_code=400, detail="Assigned user does not exist")
    updated_task = stored_task.copy(update=updated_data)
    tasks_db[id] = updated_task
    return updated_task

@app.delete("/tasks/{id}")
async def delete_task(id: int, current_user: User = Depends(get_current_user)):
    if id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks_db[id]
    return {"message": f"Task {id} deleted"}

# --- Auth Endpoint ---
@app.post("/auth/login", response_model=AuthResponse)
async def login(auth: AuthRequest):
    for user_id, user in users_db.items():
        if user.username == auth.username and user.is_active:
            if user_passwords.get(user_id) == auth.password:
                access_token = create_access_token(data={"sub": user.username})
                return AuthResponse(access_token=access_token)
            else:
                raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.post("/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    invalidated_tokens.add(token)
    return {"message": "Logout realizado com sucesso."}