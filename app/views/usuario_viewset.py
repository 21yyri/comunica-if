from rest_framework.viewsets import ReadOnlyModelViewSet
from ..models import Usuario
from ..serializers import UsuarioSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class UsuarioViewset(ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
