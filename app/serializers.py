from rest_framework import serializers
from .models import Usuario, Postagem


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
