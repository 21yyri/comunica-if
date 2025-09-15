from django.db import models
from .usuario import Usuario
from PIL import Image

class Noticia(models.Model):
    class Meta:
        verbose_name_plural: str = 'Notícias'
    
    autor: Usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    setor: str = models.CharField(max_length = 2)

    titulo: str = models.CharField(max_length = 64)
    body: str = models.TextField()

    imagem: Image = models.ImageField(blank = True, upload_to = 'noticias/')
