from rest_framework import serializers

from .models import Comentario, Mascota


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = [
            'id',
            'mascota',
            'autor',
            'contenido',
            'fecha_creacion',
        ]


class MascotaSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Mascota
        fields = [
            'id',
            'nombre',
            'descripcion',
            'imagen',
            'estado',
            'tipo_animal',
            'edad',
            'raza',
            'sexo',
            'tamano',
            'fecha_creacion',
            'fecha_actualizacion',
            'comentarios',
        ]


class MascotaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = [
            'id',
            'nombre',
            'descripcion',
            'imagen',
            'estado',
            'tipo_animal',
            'edad',
            'raza',
            'sexo',
            'tamano',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
