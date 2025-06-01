import pytest
from httpx import AsyncClient, ASGITransport
from main import app, users_collection, tasks_collection

@pytest.mark.asyncio
async def test_user_lifecycle():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Criação de usuário
        resp = await ac.post("/users", json={
            "username": "testuser",
            "email": "testuser@email.com",
            "password": "123456"
        })
        assert resp.status_code == 200
        user = resp.json()
        user_id = user["id"]

        # Login
        resp = await ac.post("/auth/login", json={
            "username": "testuser",
            "password": "123456"
        })
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get user
        resp = await ac.get(f"/users/{user_id}", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["username"] == "testuser"

        # Update user
        resp = await ac.put(f"/users/{user_id}", json={"email": "new@email.com"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "new@email.com"

        # Soft delete user
        resp = await ac.delete(f"/users/{user_id}", headers=headers)
        assert resp.status_code == 200
        
        users_collection.delete_one({"username": "testuser"})

@pytest.mark.asyncio
async def test_task_lifecycle():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Criação de usuário para tarefa
        resp = await ac.post("/users", json={
            "username": "taskuser",
            "email": "taskuser@email.com",
            "password": "123456"
        })
        user_id = resp.json()["id"]

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

        # Get task
        resp = await ac.get(f"/tasks/{task_id}", headers=headers)
        assert resp.status_code == 200

        # Update task
        resp = await ac.put(f"/tasks/{task_id}", json={"status": "fechada"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["status"] == "fechada"

        # Delete task
        resp = await ac.delete(f"/tasks/{task_id}", headers=headers)
        assert resp.status_code == 200

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