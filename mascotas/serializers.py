from rest_framework import serializers

from .models import Comentario, Mascota


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'


class MascotaSerializer(serializers.ModelSerializer):
    comentarios = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Mascota
        fields = '__all__'


class MascotaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = [
            'id',
            'nombre',
            'descripcion',
            'imagen',
            'estado',
            'fecha_creacion',
            'fecha_actualizacion',
        ]
