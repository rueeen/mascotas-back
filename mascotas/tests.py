from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Comentario, Mascota


class MascotaComentarTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mascota = Mascota.objects.create(
            nombre='Firulais',
            descripcion='Perro perdido',
            imagen='mascotas/firulais.jpg',
            estado=Mascota.Estado.PERDIDA,
        )
        self.url = f'/api/mascotas/{self.mascota.pk}/comentar/'

    def test_comentar_accepts_multipart_form_data_without_mascota_field(self):
        response = self.client.post(
            self.url,
            {
                'autor': 'Juan',
                'contenido': 'Lo vi cerca del parque.',
            },
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comentario = Comentario.objects.get()
        self.assertEqual(comentario.mascota, self.mascota)
        self.assertEqual(comentario.autor, 'Juan')
        self.assertEqual(comentario.contenido, 'Lo vi cerca del parque.')
        self.assertEqual(response.data['autor'], 'Juan')
        self.assertEqual(response.data['contenido'], 'Lo vi cerca del parque.')
        self.assertEqual(response.data['mascota'], self.mascota.pk)

    def test_comentar_accepts_json_without_mascota_field(self):
        response = self.client.post(
            self.url,
            {
                'autor': 'Ana',
                'contenido': 'Tengo más información.',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comentario = Comentario.objects.get()
        self.assertEqual(comentario.mascota, self.mascota)
        self.assertEqual(comentario.autor, 'Ana')
        self.assertEqual(comentario.contenido, 'Tengo más información.')
        self.assertEqual(response.data['autor'], 'Ana')
        self.assertEqual(response.data['contenido'], 'Tengo más información.')
        self.assertEqual(response.data['mascota'], self.mascota.pk)
