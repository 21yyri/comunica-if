from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..serializers import PostagemSerializer
from google import genai

from ..models import Usuario, Postagem

CLIENT = genai.Client()

class Postagens(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk=None):
        postagem = get_object_or_404(Postagem, id=pk)
        print(postagem.id)
        serializer = PostagemSerializer(postagem)

        return Response(serializer.data, status=200)


    def post(self, request):
        corpo, imagem = request.data.values()
        usuario = Usuario.objects.get(username=request.user)

        if not self._validar_postagem(usuario, corpo):
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


    def _validar_postagem(self, usuario, postagem):
        if usuario.is_authorized:
            return True
        
        validacao = CLIENT.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
                Verifique: ofensas (pessoais, intolerância, 
                escola, calão) ou burla (criptografia, substituições, 
                espaços). Resposta: S ou N\n\n{postagem}
            """
        ).text

        return validacao == "N"
    

    def _criar_postagem(self, usuario, corpo, imagem):
        postagem = Postagem.objects.create(
            username_usuario=usuario,
            corpo=corpo,
            imagem=imagem
        )

        return postagem
