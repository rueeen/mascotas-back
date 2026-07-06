from django.db import models


class Mascota(models.Model):
    class Estado(models.TextChoices):
        PERDIDA = 'perdida', 'Perdida'
        ENCONTRADA = 'encontrada', 'Encontrada'
        EN_ADOPCION = 'en_adopcion', 'En adopción'
        ADOPTADA = 'adoptada', 'Adoptada'

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='mascotas/')
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PERDIDA,
    )
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
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Comentario de {self.autor} en {self.mascota.nombre}'
