from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from ..models import Usuario, Noticia
from ..serializers import NoticiaSerializer


class NoticiaViewset(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


    def list(self, request):
        noticias = Noticia.objects.all()
        serializer = NoticiaSerializer(noticias, many = True)

        return Response(serializer.data, status = 200)
    

    def retrieve(self, request, pk):
        noticia = get_object_or_404(Noticia, pk = pk)
        serializer = NoticiaSerializer(noticia)

        return Response(serializer.data, status = 200)
    

    def destroy(self, request, pk):
        noticia = get_object_or_404(Noticia, pk = pk)
        noticia.delete()

        return Response({
            "msg": "Notícia deletada com sucesso."
        }, status = 200)


    @action(detail = False, methods=['post'])
    def post(self, request):
        noticia = request.data
        usuario = Usuario.objects.get(
            username = request.user
        )

        imagem = request.FILES.get("imagem")

        link = noticia.get("link")
        if self._verify_link(link):
            return Response({
                "msg": "Notícia já registrada."
            }, status = 409)

        Noticia.objects.create(
            autor = usuario,
            setor = noticia.get("setor"),
            titulo = noticia.get("titulo"),
            body = noticia.get("body"),
            imagem = imagem or None,
            link = link,
            data = noticia.get("data")
        ).save()

        return Response({
            "msg": "Notícia criada."
        }, status = 201)


    def _verify_link(self, link: str | None) -> bool:
        if link:
            noticia = Noticia.objects.filter(
                link = link
            ).first()

            return True if noticia else False
