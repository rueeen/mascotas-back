from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
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
        tipo_animal = self.request.query_params.get('tipo_animal')
        search = self.request.query_params.get('search')

        if estado:
            queryset = queryset.filter(estado=estado)
        if tipo_animal:
            queryset = queryset.filter(tipo_animal=tipo_animal)
        if search:
            queryset = queryset.filter(nombre__icontains=search)

        return queryset

    def perform_create(self, serializer):
        ip = self._get_client_ip(self.request)
        serializer.save(ip_origen=ip)

    @staticmethod
    def _get_client_ip(request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    @action(detail=True, methods=['post'], url_path='comentar')
    def comentar(self, request, pk=None):
        mascota = self.get_object()
        data = request.data.dict() if hasattr(request.data, 'dict') else dict(request.data)
        data['mascota'] = mascota.pk
        serializer = ComentarioSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        ip = self._get_client_ip(request)
        serializer.save(mascota=mascota, ip_origen=ip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def _to_options(choices_class):
    return [{'value': value, 'label': label} for value, label in choices_class.choices]


@api_view(['GET'])
@permission_classes([AllowAny])
def choices_view(request):
    return Response({
        'estado': _to_options(Mascota.Estado),
        'tipo_animal': _to_options(Mascota.TipoAnimal),
        'sexo': _to_options(Mascota.Sexo),
        'tamano': _to_options(Mascota.Tamano),
    })


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

    def perform_create(self, serializer):
        ip = MascotaViewSet._get_client_ip(self.request)
        serializer.save(ip_origen=ip)
