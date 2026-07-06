"""URL configuration for mascotas_project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from mascotas.views import ComentarioViewSet, MascotaViewSet, choices_view

router = DefaultRouter()
router.register(r'mascotas', MascotaViewSet, basename='mascota')
router.register(r'comentarios', ComentarioViewSet, basename='comentario')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/choices/', choices_view, name='choices'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
