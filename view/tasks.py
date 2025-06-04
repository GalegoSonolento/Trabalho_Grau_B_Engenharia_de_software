from fastapi import APIRouter, HTTPException, Depends
from model.models import Task, TaskCreate, TaskUpdate, User
from controller.database import tasks_collection, users_collection
from bson import ObjectId
from typing import List, Optional
import logging
from controller.auth_utils import (
    create_access_token,
    get_current_user,
    invalidated_tokens,
    oauth2_scheme
)

router = APIRouter()

@router.post("/tasks", response_model=Task)
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

@router.get("/tasks/{id}", response_model=Task)
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

@router.get("/tasks", response_model=List[Task])
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

@router.put("/tasks/{id}", response_model=Task)
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

@router.delete("/tasks/{id}")
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