import pytest
from fastapi.testclient import TestClient
#from src.main import app, get_db
from unittest.mock import MagicMock

# Mock MongoDB
@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = mock_db
    return TestClient(app)

def test_create_user(client, mock_db):
    mock_db.users.find_one.return_value = None
    mock_db.users.insert_one.return_value = MagicMock(inserted_id="12345")
    
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret"
    })
    
    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"
    mock_db.users.insert_one.assert_called()