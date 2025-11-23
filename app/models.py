from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    is_servidor = models.BooleanField(default=False)

    @property
    def is_authorized(self):
        return self.is_servidor

    def __str__(self):
        return f'{self.username}: {self.first_name} {self.last_name}'


class Postagem(models.Model):
    class Meta:
        ordering = ['-data']
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    corpo = models.TextField(max_length=300)

    imagem = models.URLField(null=True)
    data = models.DateTimeField(auto_now=True)


class Noticia(models.Model):
    class Meta:
        ordering = ['-data']

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    titulo = models.TextField(max_length=150)
    sumario = models.TextField(max_length=320)

    link = models.URLField(null=True)
    imagem = models.URLField(null=True)
    data = models.DateTimeField(auto_now=True)

    disponivel = models.BooleanField(default=True)
