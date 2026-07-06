from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Comentario, Mascota
from .serializers import ComentarioSerializer, MascotaListSerializer, MascotaSerializer


class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.prefetch_related('comentarios').all()
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.action == 'list':
            return MascotaListSerializer
        return MascotaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        search = self.request.query_params.get('search')

        if estado:
            queryset = queryset.filter(estado=estado)
        if search:
            queryset = queryset.filter(nombre__icontains=search)

        return queryset

    @action(detail=True, methods=['post'], url_path='comentar')
    def comentar(self, request, pk=None):
        mascota = self.get_object()
        data = request.data.dict() if hasattr(request.data, 'dict') else dict(request.data)
        data['mascota'] = mascota.pk
        serializer = ComentarioSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(mascota=mascota)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.select_related('mascota').all()
    serializer_class = ComentarioSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        mascota_id = self.request.query_params.get('mascota')

        if mascota_id:
            queryset = queryset.filter(mascota_id=mascota_id)

        return queryset
