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
        Noticia.objects.create(
            usuario=usuario,
            titulo=noticia["titulo"],
            sumario=noticia["sumario"],
            link=noticia["link"],
            disponivel=noticia["disponivel"],
            imagem=imagem,
            automatizado=noticia["automatizado"],
        )


    def get_imagem(self, request) -> str:
        arquivo = request.FILES.get("imagem", '')
        if arquivo:
            return upload(arquivo)
        
        return request.data["imagem"]


    def _noticia_existe(self, link: str) -> bool:
        if not link: # Evita dar como existente caso não tenha link
            return False
        
        # Verifica se há outra notícia sob esse link
        # E se ela foi inserida por script ou não
        noticia = Noticia.objects.filter(link=link).first()
        if not noticia:
            return False
        
        if noticia.automatizado == True:
            return True

        return False