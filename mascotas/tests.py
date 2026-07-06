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
        self.assertEqual(comentario.ip_origen, '127.0.0.1')
        self.assertNotIn('ip_origen', response.data)

    def test_comentar_accepts_json_without_mascota_field(self):
        response = self.client.post(
            self.url,
            {
                'autor': 'Ana',
                'contenido': 'Tengo más información.',
            },
            format='json',
            HTTP_X_FORWARDED_FOR='203.0.113.5, 198.51.100.10',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comentario = Comentario.objects.get()
        self.assertEqual(comentario.mascota, self.mascota)
        self.assertEqual(comentario.autor, 'Ana')
        self.assertEqual(comentario.contenido, 'Tengo más información.')
        self.assertEqual(response.data['autor'], 'Ana')
        self.assertEqual(response.data['contenido'], 'Tengo más información.')
        self.assertEqual(response.data['mascota'], self.mascota.pk)
        self.assertEqual(comentario.ip_origen, '203.0.113.5')
        self.assertNotIn('ip_origen', response.data)


class MascotaQueryAndSerializerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Mascota.objects.create(
            nombre='Michi',
            descripcion='Gato encontrado',
            imagen='mascotas/michi.jpg',
            estado=Mascota.Estado.ENCONTRADA,
            tipo_animal=Mascota.TipoAnimal.GATO,
            edad=2,
            raza='Mestizo',
            sexo=Mascota.Sexo.HEMBRA,
            tamano=Mascota.Tamano.PEQUENO,
            ip_origen='198.51.100.20',
        )
        Mascota.objects.create(
            nombre='Firulais',
            descripcion='Perro perdido',
            imagen='mascotas/firulais.jpg',
            estado=Mascota.Estado.PERDIDA,
            tipo_animal=Mascota.TipoAnimal.PERRO,
            ip_origen='198.51.100.21',
        )

    def test_list_filters_by_tipo_animal_and_hides_origin_ip(self):
        response = self.client.get('/api/mascotas/', {'tipo_animal': 'gato'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Michi')
        self.assertEqual(results[0]['tipo_animal'], 'gato')
        self.assertEqual(results[0]['edad'], 2)
        self.assertEqual(results[0]['raza'], 'Mestizo')
        self.assertEqual(results[0]['sexo'], 'hembra')
        self.assertEqual(results[0]['tamano'], 'pequeno')
        self.assertNotIn('ip_origen', results[0])
