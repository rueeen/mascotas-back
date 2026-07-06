from django.contrib import admin

from .models import Comentario, Mascota


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre',
        'estado',
        'tipo_animal',
        'edad',
        'sexo',
        'tamano',
        'ip_origen',
        'fecha_creacion',
        'fecha_actualizacion',
    )
    list_filter = ('estado', 'tipo_animal', 'edad', 'sexo', 'tamano')
    readonly_fields = ('ip_origen',)
    search_fields = ('nombre', 'descripcion')
    inlines = [ComentarioInline]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'mascota', 'autor', 'ip_origen', 'fecha_creacion')
    readonly_fields = ('ip_origen',)
    search_fields = ('autor', 'contenido', 'mascota__nombre')
