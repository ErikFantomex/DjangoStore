from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag


TAGS_URL = reverse('recipe:tag-list')


class TagApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='tags@example.com',
            password='testpass123',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_auth_is_required(self):
        response = APIClient().get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tags_are_limited_to_owner(self):
        Tag.objects.create(user=self.user, name='Ligera')
        other = get_user_model().objects.create_user(
            email='other-tags@example.com',
            password='testpass123',
        )
        Tag.objects.create(user=other, name='Otra')
        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Ligera')

    def test_update_and_delete_tag(self):
        tag = Tag.objects.create(user=self.user, name='Desayuno')
        url = reverse('recipe:tag-detail', args=[tag.pk])
        response = self.client.patch(url, {'name': 'Almuerzo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, 'Almuerzo')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
