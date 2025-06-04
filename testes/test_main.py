import pytest
from httpx import AsyncClient, ASGITransport
from controller.main import app
from controller.database import users_collection, tasks_collection

@pytest.mark.asyncio
async def test_create_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/users", json={
            "username": "testuser",
            "email": "testuser@email.com",
            "password": "123456"
        })
        assert resp.status_code == 200
        user = resp.json()
        assert user["username"] == "testuser"
        users_collection.delete_one({"username": "testuser"})

@pytest.mark.asyncio
async def test_login_user():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "123456",
        "is_active": True
    })
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/auth/login", json={
            "username": "testuser",
            "password": "123456"
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        users_collection.delete_one({"username": "testuser"})

@pytest.mark.asyncio
async def test_get_user():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "123456",
        "is_active": True
    })
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post("/auth/login", json={
            "username": "testuser",
            "password": "123456"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        user = users_collection.find_one({"username": "testuser"})
        user_id = str(user["_id"])
        resp = await ac.get(f"/users/{user_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["username"] == "testuser"
        users_collection.delete_one({"username": "testuser"})

@pytest.mark.asyncio
async def test_update_user():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "123456",
        "is_active": True
    })
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post("/auth/login", json={
            "username": "testuser",
            "password": "123456"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        user = users_collection.find_one({"username": "testuser"})
        user_id = str(user["_id"])
        resp = await ac.put(f"/users/{user_id}", json={"email": "new@email.com"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "new@email.com"
        users_collection.delete_one({"username": "testuser"})

@pytest.mark.asyncio
async def test_delete_user():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "testuser",
        "email": "testuser@email.com",
        "password": "123456",
        "is_active": True
    })
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post("/auth/login", json={
            "username": "testuser",
            "password": "123456"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        user = users_collection.find_one({"username": "testuser"})
        user_id = str(user["_id"])
        resp = await ac.delete(f"/users/{user_id}", headers=headers)
        assert resp.status_code == 200
        users_collection.delete_one({"username": "testuser"})

@pytest.mark.asyncio
async def test_create_task():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "taskuser",
        "email": "taskuser@email.com",
        "password": "123456",
        "is_active": True
    })
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Login
        resp = await ac.post("/auth/login", json={
            "username": "taskuser",
            "password": "123456"
        })
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Criação de tarefa
        resp = await ac.post("/tasks", json={
            "title": "Minha Tarefa",
            "description": "Descrição",
            "status": "aberta",
            "assigned_to": "taskuser"
        }, headers=headers)
        assert resp.status_code == 200
        task_id = resp.json()["id"]
        # Limpeza
        tasks_collection.delete_one({"_id": task_id})
        users_collection.delete_one({"username": "taskuser"})

@pytest.mark.asyncio
async def test_get_task():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "taskuser",
        "email": "taskuser@email.com",
        "password": "123456",
        "is_active": True
    })
    task_id = None
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Login
        resp = await ac.post("/auth/login", json={
            "username": "taskuser",
            "password": "123456"
        })
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Criação de tarefa
        resp = await ac.post("/tasks", json={
            "title": "Minha Tarefa",
            "description": "Descrição",
            "status": "aberta",
            "assigned_to": "taskuser"
        }, headers=headers)
        task_id = resp.json()["id"]
        # Buscar tarefa
        resp = await ac.get(f"/tasks/{task_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Minha Tarefa"
        # Limpeza
        tasks_collection.delete_one({"_id": task_id})
        users_collection.delete_one({"username": "taskuser"})

@pytest.mark.asyncio
async def test_get_tasks():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "taskuser",
        "email": "taskuser@email.com",
        "password": "123456",
        "is_active": True
    })
    task_id = None
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Login
        resp = await ac.post("/auth/login", json={
            "username": "taskuser",
            "password": "123456"
        })
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Criação de tarefa
        resp = await ac.post("/tasks", json={
            "title": "Minha Tarefa",
            "description": "Descrição",
            "status": "aberta",
            "assigned_to": "taskuser"
        }, headers=headers)
        task_id = resp.json()["id"]
        # Buscar tarefa
        resp = await ac.get(f"/tasks", headers=headers)
        assert resp.status_code == 200
        #assert resp.json()["title"] == "Minha Tarefa"
        # Limpeza
        tasks_collection.delete_one({"_id": task_id})
        users_collection.delete_one({"username": "taskuser"})

@pytest.mark.asyncio
async def test_update_task():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "taskuser",
        "email": "taskuser@email.com",
        "password": "123456",
        "is_active": True
    })
    task_id = None
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Login
        resp = await ac.post("/auth/login", json={
            "username": "taskuser",
            "password": "123456"
        })
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Criação de tarefa
        resp = await ac.post("/tasks", json={
            "title": "Minha Tarefa",
            "description": "Descrição",
            "status": "aberta",
            "assigned_to": "taskuser"
        }, headers=headers)
        task_id = resp.json()["id"]
        # Atualizar tarefa
        resp = await ac.put(f"/tasks/{task_id}", json={"status": "fechada"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "fechada"
        # Limpeza
        tasks_collection.delete_one({"_id": task_id})
        users_collection.delete_one({"username": "taskuser"})

@pytest.mark.asyncio
async def test_delete_task():
    transport = ASGITransport(app=app)
    users_collection.insert_one({
        "username": "taskuser",
        "email": "taskuser@email.com",
        "password": "123456",
        "is_active": True
    })
    task_id = None
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Login
        resp = await ac.post("/auth/login", json={
            "username": "taskuser",
            "password": "123456"
        })
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Criação de tarefa
        resp = await ac.post("/tasks", json={
            "title": "Minha Tarefa",
            "description": "Descrição",
            "status": "aberta",
            "assigned_to": "taskuser"
        }, headers=headers)
        task_id = resp.json()["id"]
        # Deletar tarefa
        resp = await ac.delete(f"/tasks/{task_id}", headers=headers)
        assert resp.status_code == 200
        # Limpeza
        users_collection.delete_one({"username": "taskuser"})
        tasks_collection.delete_many({"assigned_to": "taskuser"})

@pytest.mark.asyncio
async def test_auth_logout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Criação de usuário
        await ac.post("/users", json={
            "username": "logoutuser",
            "email": "logout@email.com",
            "password": "123456"
        })
        # Login
        resp = await ac.post("/auth/login", json={
            "username": "logoutuser",
            "password": "123456"
        })
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Logout
        resp = await ac.post("/auth/logout", headers=headers)
        assert resp.status_code == 200

        # Tenta acessar endpoint protegido após logout
        resp = await ac.get("/users/invalidid", headers=headers)
        assert resp.status_code == 401 or resp.status_code == 400

        users_collection.delete_one({"username": "logoutuser"})