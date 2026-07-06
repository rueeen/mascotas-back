from django.contrib import admin

from .models import Comentario, Mascota


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('estado',)
    search_fields = ('nombre', 'descripcion')
    inlines = [ComentarioInline]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'mascota', 'autor', 'fecha_creacion')
    search_fields = ('autor', 'contenido', 'mascota__nombre')
