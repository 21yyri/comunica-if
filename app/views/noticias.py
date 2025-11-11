from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from ..serializers import NoticiaSerializer
from ..models import Usuario, Noticia

class Noticias(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk=None):
        noticia = get_object_or_404(Noticia, pk=pk)
        serializer = NoticiaSerializer(noticia)

        return Response(serializer.data, status=200)


    def post(self, request):
        noticia = request.data
        usuario = Usuario.objects.get(username=request.user)

        if not usuario.is_authorized:
            return Response({
                "msg": "Usuário não autorizado para criar notícias."
            }, status=403)
        
        self._criar_noticia(usuario, noticia)

        return Response({
            "msg": "Notícia criada com sucesso."
        }, status=201)

    
    def _criar_noticia(self, usuario, noticia):
        Noticia.objects.create(
            username_usuario=usuario,
            titulo=noticia["titulo"],
            sumario=noticia["sumario"],
            link=noticia["link"],
            disponivel=noticia["disponivel"]
        )
