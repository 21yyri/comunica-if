from rest_framework.viewsets import ReadOnlyModelViewSet
from ..models import Usuario
from ..serializers import UsuarioSerializer
from ..authorization import BearerTokenAuth
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UsuarioViewset(ReadOnlyModelViewSet):
    authentication_classes = [BearerTokenAuth]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
