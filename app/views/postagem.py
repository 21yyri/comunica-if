from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import PostagemSerializer
from ..models import Usuario, Postagem

from ..services.post_authorization import validar_postagem
from ..services.image_upload import upload

class Postagens(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk=None):
        postagem = get_object_or_404(Postagem, id=pk)
        serializer = PostagemSerializer(postagem)

        return Response(serializer.data, status=200)


    def post(self, request):
        corpo, imagem = request.data.values()
        usuario = Usuario.objects.get(username=request.user)

        if imagem:
            imagem = upload(imagem)

        if not validar_postagem(usuario, corpo):
            return Response({
                "msg": "Erro ao validar a postagem."
            }, status=400)
        
        self._criar_postagem(usuario, corpo, imagem)
        return Response({
            "msg": "Postagem criada com sucesso."
        }, status=201)
    

    def delete(self, request, pk):
        postagem = get_object_or_404(Postagem, pk=pk)
        usuario = Usuario.objects.get(username=request.user)

        if usuario.is_servidor:
            postagem.delete()
        
            return Response({
                "msg": "Postagem deletada com sucesso."
            }, 200)
        
        if usuario.pk != postagem.username_usuario:
            return Response({
                "Você não pode remover postagens alheias."
            }, 400)
        
        postagem.delete()
        return Response({
            "msg": "Postagem deletada com sucesso."
        }, 200)


    def _criar_postagem(self, usuario, corpo, imagem):
        postagem = Postagem.objects.create(
            usuario=usuario,
            corpo=corpo,
            imagem=imagem or None
        )

        return postagem
 