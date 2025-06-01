from django.test import TestCase
from django.urls import reverse
from usuarios.views import lista_usuarios


class TestesUsuarios(TestCase):
    def testa_lista_usuarios(self):
        response = self.client.get(reverse('lista_usuarios'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['usuarios']), 2)