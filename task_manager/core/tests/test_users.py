import pytest
from rest_framework.test import APIClient
from rest_framework import status
from core.models import User

@pytest.mark.django_db
class TestUserAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_create_user(self):
        response = self.client.post('/api/users/', self.user_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == self.user_data['username']
        assert User.objects.filter(username=self.user_data['username']).exists()

    def test_get_user(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        response = self.client.get(f'/api/users/{user.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == self.user_data['username']

    def test_update_user(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        update_data = {'first_name': 'Updated'}
        response = self.client.put(f'/api/users/{user.id}/', update_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'

    def test_delete_user(self):
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/{user.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.get(id=user.id).is_deleted