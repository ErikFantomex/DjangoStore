"""
Pruebas para Django administrador notificacion
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTest(TestCase):
    """
    Pruebas para el administrador de Django
    """
    def setUp(self):
        """creando el usuario y el cliente"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@example.com',
            password = 'testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'user@example.com',
            password = 'testpass123',
            name = 'Test User'
        )

    def test_users_list(self):
        """Pruebas para usuarios listados en la pagina"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res,self.user.name)
        self.assertContains(res,self.user.email)

    def test_edit_user_page(self):
        """Prueba para editar pagina de usuario que funciona"""
        url = reverse('admin:core_user_change',args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)

    def test_create_user_page(self):
        """Prueba para crear pagina de usuario que funciona"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code,200)
        

