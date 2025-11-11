from rest_framework import serializers
from .models import Postagem, Noticia


class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postagem
        fields = "__all__"


class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = "__all__"
