from django.core.files.uploadedfile import SimpleUploadedFile
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

    def test_list_returns_all_mascotas_and_hides_origin_ip(self):
        response = self.client.get('/api/mascotas/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if isinstance(response.data, dict) and 'results' in response.data else response.data
        self.assertEqual(len(results), 2)
        michi = next(result for result in results if result['nombre'] == 'Michi')
        self.assertEqual(michi['tipo_animal'], 'gato')
        self.assertEqual(michi['edad'], 2)
        self.assertEqual(michi['raza'], 'Mestizo')
        self.assertEqual(michi['sexo'], 'hembra')
        self.assertEqual(michi['tamano'], 'pequeno')
        self.assertNotIn('ip_origen', michi)

    @staticmethod
    def _test_image(name='mascota.gif'):
        return SimpleUploadedFile(
            name,
            b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;',
            content_type='image/gif',
        )

    def test_create_saves_origin_ip_and_hides_it_in_response(self):
        response = self.client.post(
            '/api/mascotas/',
            {
                'nombre': 'Luna',
                'descripcion': 'Gata perdida cerca de la escuela',
                'imagen': self._test_image(),
                'estado': Mascota.Estado.PERDIDA,
            },
            format='multipart',
            REMOTE_ADDR='203.0.113.45',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mascota = Mascota.objects.get(nombre='Luna')
        self.assertEqual(mascota.ip_origen, '203.0.113.45')
        self.assertNotIn('ip_origen', response.data)

    def test_detail_hides_origin_ip(self):
        mascota = Mascota.objects.get(nombre='Michi')

        response = self.client.get(f'/api/mascotas/{mascota.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Michi')
        self.assertNotIn('ip_origen', response.data)

    def test_create_accepts_optional_detail_fields_and_saves_them(self):
        response = self.client.post(
            '/api/mascotas/',
            {
                'nombre': 'Toby',
                'descripcion': 'Perro en adopción',
                'imagen': self._test_image('toby.gif'),
                'estado': Mascota.Estado.EN_ADOPCION,
                'tipo_animal': Mascota.TipoAnimal.PERRO,
                'edad': 4,
                'raza': 'Labrador',
                'sexo': Mascota.Sexo.MACHO,
                'tamano': Mascota.Tamano.GRANDE,
            },
            format='multipart',
            REMOTE_ADDR='198.51.100.77',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mascota = Mascota.objects.get(nombre='Toby')
        self.assertEqual(mascota.tipo_animal, Mascota.TipoAnimal.PERRO)
        self.assertEqual(mascota.edad, 4)
        self.assertEqual(mascota.raza, 'Labrador')
        self.assertEqual(mascota.sexo, Mascota.Sexo.MACHO)
        self.assertEqual(mascota.tamano, Mascota.Tamano.GRANDE)
        self.assertEqual(response.data['edad'], 4)
        self.assertEqual(response.data['raza'], 'Labrador')
        self.assertEqual(response.data['sexo'], 'macho')
        self.assertEqual(response.data['tamano'], 'grande')
        self.assertNotIn('ip_origen', response.data)


class MascotaChoicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_choices_endpoint_returns_mascota_catalogs(self):
        response = self.client.get('/api/choices/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data.keys()),
            {'estado', 'tipo_animal', 'sexo', 'tamano'},
        )
        for key in ('estado', 'tipo_animal', 'sexo', 'tamano'):
            self.assertIsInstance(response.data[key], list)
            self.assertGreater(len(response.data[key]), 0)
            for option in response.data[key]:
                self.assertEqual(set(option.keys()), {'value', 'label'})

        self.assertEqual(
            [option['value'] for option in response.data['estado']],
            ['perdida', 'encontrada', 'en_adopcion', 'adoptada'],
        )
