from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from ..models import Usuario, Noticia


class NoticiaViewset(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        noticia = request.data
        usuario = Usuario.objects.get(
            username = request.user
        )

        imagem = request.FILES.get("imagem")
        Noticia.objects.create(
            autor = usuario,
            setor = noticia.get("setor"),
            titulo = noticia.get("titulo"),
            body = noticia.get("body"),
            imagem = imagem or None
        ).save()

        return Response({
            "msg": "Notícia criada."
        }, status = 201)
