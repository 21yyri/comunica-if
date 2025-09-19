from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from ..authorization import BearerTokenAuth
from rest_framework.permissions import IsAuthenticated
from ..models import Usuario, Postagem
from ..serializers import PostagemSerializer
from google.genai.errors import ServerError
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()


class PostagemViewset(ViewSet):
    authentication_classes = [BearerTokenAuth]
    permission_classes = [IsAuthenticated]


    def list(self, request):
        postagem = Postagem.objects.all()
        serializer = PostagemSerializer(postagem, many = True)
        
        return Response(serializer.data, status = 200)


    def retrieve(self, request, pk = None):
        postagem = get_object_or_404(Postagem, pk = pk)
        serializer = PostagemSerializer(postagem)

        return Response(serializer.data, status = 200)


    def destroy(self, request, pk):
        postagem = get_object_or_404(Postagem, pk = pk)
        
        usuario = Usuario.objects.get(
            pk = postagem.autor_id
        ).__str__()

        if not usuario == request.user.username:
            return Response({
                "msg": "Não é possível deletar postagem."
            }, 403)
        
        postagem.delete()

        return Response({
            "msg": "Postagem deletada."
        }, status = 200)
    

    @action(detail = False, methods=['post'])
    def post(self, request: Request):
        postagem = request.data.get("body")
        usuario = Usuario.objects.get(
            username = request.user
        )

        # Validação do conteúdo da postagem
        try:
            autorizacao = self._verify_post(postagem)
        except ServerError:
            return Response({
                "msg": "Autorização interminada por excesso de requisições ao servidor."
            }, status = 503)
        
        if not autorizacao:
            return Response({
                "msg": "Postagem não passou na validação."
            }, status = 400)
        
        # Criação da postagem
        imagem = request.FILES.get("imagem")
        Postagem.objects.create(
            autor = usuario,
            body = postagem,
            imagem = imagem or None 
        ).save()

        return Response({
            "msg": "Postagem foi verificada e autorizada."
        }, status = 201)


    def _verify_post(self, postagem) -> bool:
        """Retorna o resultado da validação do conteúdo da postagem."""
        auth = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = f"""
                Verifique: ofensas (pessoais, intolerância, 
                escola, calão) ou burla (criptografia, substituições, 
                espaços). Resposta: S ou N\n\n{postagem}"""
        ).text

        return auth == "N"
