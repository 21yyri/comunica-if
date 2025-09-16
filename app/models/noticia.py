from django.db import models
from .usuario import Usuario
from datetime import datetime
from PIL import Image

class Noticia(models.Model):
    class Meta:
        verbose_name_plural: str = 'Notícias'
    
    autor: Usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    setor: str = models.CharField(max_length = 15)

    titulo: str = models.CharField(max_length = 150)
    body: str = models.TextField()

    imagem: Image = models.ImageField(blank = True, upload_to = 'noticias/')
    link: str = models.CharField(max_length = 220, default = None)

    data: datetime = models.DateTimeField(auto_now = True)
