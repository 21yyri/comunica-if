from rest_framework import serializers
from .models import Usuario, Postagem, Noticia


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'nome_completo',
            'email'
        ]


class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postagem
        fields = [
            'id',
            'body',
            'data'
        ]


class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = [
            'id', 'autor', 
            'setor', 'titulo', 
            'body', 'imagem'
        ]