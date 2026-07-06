from django.db import models


class Mascota(models.Model):
    class Estado(models.TextChoices):
        PERDIDA = 'perdida', 'Perdida'
        ENCONTRADA = 'encontrada', 'Encontrada'
        EN_ADOPCION = 'en_adopcion', 'En adopción'
        ADOPTADA = 'adoptada', 'Adoptada'

    class TipoAnimal(models.TextChoices):
        PERRO = 'perro', 'Perro'
        GATO = 'gato', 'Gato'
        AVE = 'ave', 'Ave'
        ROEDOR = 'roedor', 'Roedor'
        REPTIL = 'reptil', 'Reptil'
        OTRO = 'otro', 'Otro'

    class Sexo(models.TextChoices):
        MACHO = 'macho', 'Macho'
        HEMBRA = 'hembra', 'Hembra'
        DESCONOCIDO = 'desconocido', 'Desconocido'

    class Tamano(models.TextChoices):
        PEQUENO = 'pequeno', 'Pequeño'
        MEDIANO = 'mediano', 'Mediano'
        GRANDE = 'grande', 'Grande'
        DESCONOCIDO = 'desconocido', 'Desconocido'

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mascotas/')
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PERDIDA,
    )
    tipo_animal = models.CharField(
        max_length=20,
        choices=TipoAnimal.choices,
        default=TipoAnimal.OTRO,
    )
    edad = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Edad aproximada en años, si se conoce',
    )
    raza = models.CharField(max_length=100, blank=True, default='')
    sexo = models.CharField(
        max_length=20,
        choices=Sexo.choices,
        blank=True,
        default=Sexo.DESCONOCIDO,
    )
    tamano = models.CharField(
        max_length=20,
        choices=Tamano.choices,
        blank=True,
        default=Tamano.DESCONOCIDO,
    )
    ip_origen = models.GenericIPAddressField(null=True, blank=True, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.nombre} ({self.get_estado_display()})'


class Comentario(models.Model):
    mascota = models.ForeignKey(
        Mascota,
        related_name='comentarios',
        on_delete=models.CASCADE,
    )
    autor = models.CharField(max_length=100)
    contenido = models.TextField()
    ip_origen = models.GenericIPAddressField(null=True, blank=True, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Comentario de {self.autor} en {self.mascota.nombre}'
