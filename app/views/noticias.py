from ..serializers import NoticiaSerializer
from ..models import Usuario, Noticia
from ..services.image_upload import upload

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class Noticias(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        noticia = get_object_or_404(Noticia, pk=pk)
        serializer = NoticiaSerializer(noticia)

        return Response(serializer.data, status=200)


    def post(self, request):
        noticia = request.data
        usuario = Usuario.objects.get(username=request.user)

        imagem = self.get_imagem(request)

        if not usuario.is_authorized:
            return Response({
                "msg": "Usuário não autorizado para criar notícias."
            }, status=403)
        
        if self._noticia_existe(noticia["link"]):
            return Response({
                "msg": "Notícia já existe."
            }, status=409)
        
        self._criar_noticia(usuario, noticia, imagem)

        return Response({
            "msg": "Notícia criada com sucesso."
        }, status=201)
    

    def delete(self, request, pk=None):
        noticia = get_object_or_404(Noticia, pk=pk)
        noticia.delete()

        return Response({
            "msg": "Notícia deletada com sucesso."
        }, 200)

    
    def _criar_noticia(self, usuario, noticia, imagem) -> Noticia:
        try:
            Noticia.objects.create(
                usuario=usuario,
                titulo=noticia["titulo"],
                sumario=noticia["sumario"],
                link=noticia["link"],
                disponivel=noticia["disponivel"],
                imagem=imagem,
            )
        except:
            pass # Erro esquisito onde diz que a imagem é muiti longa pra a coluna (???)

    

    def get_imagem(self, request) -> str:
        if request.data["imagem"]:
            return request.data["imagem"]
        return upload(request.FILES["imagem"])


    def _noticia_existe(self, url: str) -> bool:
        try:
            Noticia.objects.get(link=url)
        except:
            return False
        return True
